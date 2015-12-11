import plotly

print(plotly.__version__)  # version 1.9.x required
plotly.offline.init_notebook_mode()  # run at the start of every notebook

from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import cufflinks as cf
import pandas as pd

cf.set_config_file(offline=True, world_readable=False)


def process_fields(data_dict):
    for key in data_dict.keys():
        if 'median_rent' in data_dict[key].columns and 'median_price' in data_dict[key].columns:
            data_dict[key]['gross_yield_pct'] = data_dict[key]['median_rent'] * 12 / data_dict[key][
                'median_price'] * 100
            data_dict[key] = data_dict[key].sort('gross_yield_pct', ascending=False)
    return data_dict


def join(this, other, on=None):
    return pd.merge(this, other, left_on=on, right_on=on)


def split(data, top_pct=20, max_num_of_entries=25):
    top_index = min(int(len(data) * top_pct), max_num_of_entries)
    return [data[:top_index], data[top_index:]]


class Summarizer:
    def __init__(self, data=None, **kwargs):
        """
        Args:
            data: dict, {main: main_data, population: population_data, ...}
            **kwargs:

        Returns:

        """
        self.data = process_fields(data)
        self.configs = dict()
        self._update_configs(**kwargs)

    def reset(self, data=None, **kwargs):
        if data is not None:
            self.data = process_fields(data)
        self._update_configs(**kwargs)

    def plot_scatters(self, requirements=None):
        """
        A scatter plot (subplots) for the current data.
        Args:
            requirements: list of dicts, [dict(x=str, y=str, data=str, name=str, text_field=str, split=list, join=boolean, join_left=str, join_right=str, join_on=str, size=int)]

        Returns:

        """

        num_of_plots = len(requirements)
        nrows = int((num_of_plots + 1) / 2)
        ncols = min(int(num_of_plots / nrows), 2)

        traces = []
        titles = []
        for item in requirements:
            titles.append(item['x'] + ' vs. ' + item['y'])
            if 'text_field' not in item:
                item['text_field'] = item['join_on']

            if 'join' in item and item['join']:
                joined = join(self.data[item['join_left']], self.data[item['join_right']], on=item['join_on'])
                params = dict(x=joined[item['x']].values.astype(int),
                              y=joined[item['y']].values.astype(float),
                              name=item['name'],
                              mode='markers',
                              text=joined.county.values)
                if 'size' in item:
                    params.update(marker=dict(size=item['size']))
                traces.append(go.Scatter(**params))

            elif 'split' in item and len(item['split']) > 1:
                split_data_list = split(self.data[item['data']],
                                        top_pct=self.configs['top_percentage'],
                                        max_num_of_entries=self.configs['max_num_of_entries'])
                for entry, name in zip(split_data_list, item['split']):
                    traces.append(go.Scatter(x=entry[item['data']][item['x']].values.astype(float),
                                             y=entry[item['data']][item['y']].values.astype(float),
                                             mode='markers',
                                             name=name,
                                             text=entry[item['data']][item['text_field']].values))

            else:
                traces.append(go.Scatter(x=self.data[item['data']][item['x']].values.astype(float),
                                         y=self.data[item['data']][item['y']].values.astype(float),
                                         mode='markers',
                                         name=item['name'],
                                         text=self.data[item['data']][item['text_field']].values))

        fig = tools.make_subplots(rows=nrows, cols=ncols, subplot_titles=titles)

        for trace in traces:
            fig.append_trace(trace, 1, 1)
        fig.append_trace(trace2, 1, 1)
        fig.append_trace(trace3, 1, 2)

        # All of the axes properties here: https://plot.ly/python/reference/#XAxis
        fig['layout']['xaxis1'].update(title='Median Price $')
        fig['layout']['xaxis2'].update(title='County Population', type='log')

        # All of the axes properties here: https://plot.ly/python/reference/#YAxis
        fig['layout']['yaxis1'].update(title='Median Monthly Rent')
        fig['layout']['yaxis2'].update(title='Gross Yield (%)')  # , range=[40, 80])

        fig['layout'].update(title='Visualizing County Returns')
        plotly.offline.iplot(fig)

    def plot_time_series(self, hash_key, plot_field=None):
        pass

    def _update_configs(self, **kwargs):
        self.configs.update(**kwargs)
