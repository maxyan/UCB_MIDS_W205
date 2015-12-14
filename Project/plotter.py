import cufflinks as cf
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
from plotly import tools

from UCB_MIDS_W205.Project.api.great_schools import GreatSchools
from UCB_MIDS_W205.Project.api.population import Population
from UCB_MIDS_W205.Project.data_models import Datamodel
from UCB_MIDS_W205.Project.mission_control import MissionControl
from UCB_MIDS_W205.Project.postgresql_handler import Postgresql

print(plotly.__version__)  # version 1.9.x required
plotly.offline.init_notebook_mode()  # run at the start of every notebook
cf.set_config_file(offline=True, world_readable=False)


class Plotter:
    def __init__(self, min_price=150000, max_price=300000, top_percentage=0.25, top_max_num_entries=30):
        self.MIN_PRICE = min_price
        self.MAX_PRICE = max_price
        self.TOP_PERCENTAGE = top_percentage
        self.TOP_MAX_NUM_ENTRIES = top_max_num_entries

        datamodel = Datamodel()
        self.time_series_postgres = self._initialize_postgres(datamodel.zipcode_timeseries())
        self.population_postgres = self._initialize_postgres(datamodel.population())
        self.great_schools_postgres = self._initialize_postgres(datamodel.great_schools())

        self.zipcode_timeseries = None
        self.top_zipcodes_timeseries = None
        self.rest_zipcodes_timeseries = None
        self.top_zipcodes_school_data = None
        self.top_zipcodes_population_data = None
        self.all_months_timeseries = None

    def reset(self):
        self.zipcode_timeseries = None
        self.top_zipcodes_timeseries = None
        self.rest_zipcodes_timeseries = None
        self.top_zipcodes_school_data = None
        self.top_zipcodes_population_data = None
        self.all_months_timeseries = None

    def _get_time_series_data(self, year_month=201510):
        suitable_states = self.time_series_postgres.get(
            "select * from {table} where year_month={year_month} and median_price < {max_price} and median_price > {min_price}".format(
                table=self.time_series_postgres.table,
                year_month=year_month,
                max_price=self.MAX_PRICE,
                min_price=self.MIN_PRICE))

        suitable_states['gross_yield_pct'] = suitable_states.median_rent * 12 / suitable_states.median_price * 100
        suitable_states = suitable_states.sort('gross_yield_pct', ascending=False)
        top_index = min(int(len(suitable_states) * self.TOP_PERCENTAGE), self.TOP_MAX_NUM_ENTRIES)

        self.zipcode_timeseries = suitable_states
        self.top_zipcodes_timeseries = suitable_states[:top_index]
        self.rest_zipcodes_timeseries = suitable_states[top_index:]

    def _get_population_data(self):
        if self.top_zipcodes_timeseries is None:
            self._get_time_series_data()
        p = Population(recreate=False)
        self.top_zipcodes_population_data = p.run(addresses=self.top_zipcodes_timeseries.zip_code.values)

    def _get_top_zipcodes_school_data(self):
        all_states = self.top_zipcodes_timeseries.state.values
        all_zipcodes = self.top_zipcodes_timeseries.zip_code.values
        unique_states = self.top_zipcodes_timeseries.state.unique()

        requests = []
        for state in unique_states:
            unique_zipcodes = np.unique(all_zipcodes[all_states == state])
            for zip_code in unique_zipcodes:
                requests.append(dict(db_configs=dict(postgres=self.great_schools_postgres,
                                                     query="select * from {table} where state='{state}' and zip_code={zip_code};".format(
                                                         table=self.great_schools_postgres.table,
                                                         state=state,
                                                         zip_code=zip_code)),
                                     api_configs=dict(api=GreatSchools,
                                                      api_key=None,
                                                      api_args=dict(state=state, zip_code=zip_code, limit=20)
                                                      )
                                     )
                                )
        mission_control = MissionControl()
        gs_data = mission_control.request_data(user_requests=requests)
        gs_data_df = pd.DataFrame()
        for entry in gs_data:
            gs_data_df = gs_data_df.append(entry)
        self.top_zipcodes_school_data = pd.DataFrame(gs_data_df.groupby('zip_code')['gsrating'].mean())
        self.top_zipcodes_school_data['zip_code'] = self.top_zipcodes_school_data.index

    def _initialize_postgres(self, (table, config)):
        postgres = Postgresql(user_name='postgres', password='postgres', host='localhost', port='5432',
                              db='TestProject')
        postgres.initialize_table(table, recreate=False, **config)
        return postgres

    def plot_zipcode_yield_fluctuation(self):
        if self.top_zipcodes_timeseries is None:
            self._get_time_series_data()
        if self.all_months_timeseries is None:
            self._get_all_months_timeseries()
        self._box_plot(values='gross_yield_pct', normalize=False)

    def _box_plot(self, values=None, normalize=False):
        ts_pivot = self.all_months_timeseries.pivot(index='year_month', columns='key', values=values)
        ts_pivot = ts_pivot.T
        if normalize:
            ts_pivot['fluctuation'] = (ts_pivot.max(axis=1) - ts_pivot.min(axis=1)) / ts_pivot.max(axis=1)
        else:
            ts_pivot['fluctuation'] = ts_pivot.max(axis=1) - ts_pivot.min(axis=1)
        ts_pivot = ts_pivot.sort('fluctuation').drop('fluctuation', axis=1)
        ts_pivot.T.iplot(kind='box', filename='cufflinks/box-plots',
                         title='Fluctuations of {field} - Top Zipcodes'.format(field=values))

    def _get_all_months_timeseries(self):
        self.all_months_timeseries = self.time_series_postgres.get(
            "select * from {table} where zip_code in {zip_codes};".format(table=self.time_series_postgres.table,
                                                                          zip_codes=str(
                                                                              tuple(
                                                                                  self.top_zipcodes_timeseries.zip_code.values))))
        self.all_months_timeseries[
            'gross_yield_pct'] = self.all_months_timeseries.median_rent * 12 / self.all_months_timeseries.median_price * 100
        self.all_months_timeseries['key'] = self.all_months_timeseries['zip_code'].astype(str) + ', ' + \
                                            self.all_months_timeseries['state']
        self.all_months_timeseries = self.all_months_timeseries[
            ['key', 'gross_yield_pct', 'median_price', 'year_month']]
        self.all_months_timeseries['gross_yield_pct'] = self.all_months_timeseries['gross_yield_pct'].values.astype(
            float)

    def plot_zipcode_price_fluctuation(self):
        if self.top_zipcodes_timeseries is None:
            self._get_time_series_data()
        if self.all_months_timeseries is None:
            self._get_all_months_timeseries()
        self._box_plot(values='median_price', normalize=True)

    def plot_top_zipcode_schools(self, selected_zip_codes=None):
        if self.top_zipcodes_timeseries is None:
            self._get_time_series_data()
        if self.top_zipcodes_school_data is None:
            self._get_top_zipcodes_school_data()

        top_results_school = self.top_zipcodes_timeseries.join(self.top_zipcodes_school_data,
                                                               on='zip_code',
                                                               lsuffix='',
                                                               rsuffix='_r')
        fig = tools.make_subplots(rows=1,
                                  cols=1,
                                  subplot_titles=['Yield vs. School Rating'])
        trace1 = go.Scatter(x=top_results_school.gross_yield_pct.values.astype(float),
                            y=top_results_school.gsrating.values.astype(float),
                            mode='markers',
                            name='Top Return Zipcodes',
                            marker=dict(size=10, color='green'),
                            text=top_results_school.zip_code.astype(
                                str) + ', ' + top_results_school.county.values + ', ' + top_results_school.state.values)
        fig.append_trace(trace1, 1, 1)

        if selected_zip_codes:
            selected_results = top_results_school.loc[top_results_school.zip_code.isin(selected_zip_codes)]
            trace2 = go.Scatter(x=selected_results.gross_yield_pct.values.astype(float),
                                y=selected_results.gsrating.values.astype(float),
                                mode='markers',
                                name='Top Return Zipcodes',
                                marker=dict(size=10),
                                text=selected_results.zip_code.astype(
                                    str) + ', ' + selected_results.county.values + ', ' + selected_results.state.values)
            fig.append_trace(trace2, 1, 1)

        # All of the axes properties here: https://plot.ly/python/reference/#XAxis
        fig['layout']['xaxis1'].update(title='Gross Yield (%)')

        # All of the axes properties here: https://plot.ly/python/reference/#YAxis
        fig['layout']['yaxis1'].update(title='Average School Rating')
        plotly.offline.iplot(fig)

    def plot_zipcode_overview(self, selected_zip_codes=None):
        if self.top_zipcodes_timeseries is None:
            self._get_time_series_data()
        if self.top_zipcodes_population_data is None:
            self._get_population_data()

        join_results = pd.merge(self.top_zipcodes_timeseries,
                                self.top_zipcodes_population_data,
                                left_on='zip_code',
                                right_on='zip_code',
                                suffixes=('_l', '_r'))
        join_results['key'] = join_results['zip_code'].astype(str) + ', ' + join_results['closest_city'].astype(str)
        join_results = join_results.loc[join_results.closest_city != 'NULL']

        trace1 = go.Scatter(x=self.rest_zipcodes_timeseries.median_price.values.astype(float),
                            y=self.rest_zipcodes_timeseries.median_rent.values.astype(float),
                            mode='markers',
                            name='Rest',
                            text=self.rest_zipcodes_timeseries.zip_code.astype(
                                str) + ', ' + self.rest_zipcodes_timeseries.state)

        trace2 = go.Scatter(x=self.top_zipcodes_timeseries.median_price.values.astype(float),
                            y=self.top_zipcodes_timeseries.median_rent.values.astype(float),
                            mode='markers',
                            name='Top',
                            text=self.top_zipcodes_timeseries.zip_code.astype(
                                str) + ', ' + self.top_zipcodes_timeseries.state)

        trace3 = go.Scatter(x=join_results.closest_city_population.values.astype(int),
                            y=join_results.gross_yield_pct.values.astype(float),
                            name='Population',
                            mode='markers',
                            marker=dict(size=10),
                            text=join_results.key.values)

        if selected_zip_codes:
            selected_results = join_results.loc[join_results.zip_code.isin(selected_zip_codes)]
            trace4 = go.Scatter(x=selected_results['closest_city_population'].values.astype(int),
                                y=selected_results['gross_yield_pct'].values.astype(float),
                                name='Population - Selected Zipcodes',
                                mode='markers',
                                marker=dict(size=10),
                                text=selected_results.key.values)

        fig = tools.make_subplots(rows=1,
                                  cols=2,
                                  subplot_titles=['Price vs. Rent',
                                                  'Yield vs. Population - Top Zipcodes'])

        fig.append_trace(trace1, 1, 1)
        fig.append_trace(trace2, 1, 1)
        fig.append_trace(trace3, 1, 2)
        if selected_zip_codes:
            fig.append_trace(trace4, 1, 2)

        # All of the axes properties here: https://plot.ly/python/reference/#XAxis
        fig['layout']['xaxis1'].update(title='Median Price $')
        fig['layout']['xaxis2'].update(title='Population of closest major city', type='log')

        # All of the axes properties here: https://plot.ly/python/reference/#YAxis
        fig['layout']['yaxis1'].update(title='Median Monthly Rent')
        fig['layout']['yaxis2'].update(title='Gross Yield (%)')

        fig['layout'].update(title='Visualizing Zipcode Returns')
        plotly.offline.iplot(fig)
