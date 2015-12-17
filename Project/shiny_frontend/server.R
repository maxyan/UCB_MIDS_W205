library(shiny)
library(ggplot2)
library(plyr)

# myan: this block of code only runs once when the app is launched and will not change for multiple user connections
all_timeseries = read.csv("all_timeseries.csv")
all_timeseries$gross_yield = all_timeseries$median_rent * 12 / all_timeseries$median_price * 100
all_timeseries = all_timeseries[!is.na(all_timeseries$gross_yield) 
                                & !is.nan(all_timeseries$gross_yield) 
                                & !is.null(all_timeseries$gross_yield), ]
all_timeseries = all_timeseries[order(-all_timeseries$gross_yield), ]

all_population = read.csv("all_population.csv")
all_population = all_population[!is.na(all_population$closest_city_population) 
                                & !is.nan(all_population$closest_city_population) 
                                & !is.null(all_population$closest_city_population), ]

all_schools = read.csv("all_schools.csv")
all_schools = all_schools[!is.na(all_schools$gsrating) 
                          & !is.nan(all_schools$gsrating) 
                          & !is.null(all_schools$gsrating), ]
zip_code_rating = aggregate(all_schools$gsrating, list(zip_code=all_schools$zip_code), mean)
zip_code_rating = rename(zip_code_rating, c("x"="avg_gsrating"))


shinyServer(
  function(input, output) {
    output$price_rent <- renderPlot({
      selected = all_timeseries[all_timeseries$year_month == input$year_month 
                                & all_timeseries$median_price >= input$price_range[1]
                                & all_timeseries$median_price <= input$price_range[2], ]
      selected$group = 'Rest'
      top_index = min(input$top_max_num_entries, dim(selected)[1] * input$top_percentage)
      selected$group[1:top_index] = 'Top'
      
      ggplot(selected, aes(x=median_price, y=median_rent, color=group)) +
        geom_point(shape=1) +
        scale_colour_hue(l=50) + # Use a slightly darker palette than normal
        geom_smooth(method=lm,   # Add linear regression lines
                    se=FALSE)
    })
    
    output$price_rent_info <- renderText({
      selected = all_timeseries[all_timeseries$year_month == input$year_month 
                                & all_timeseries$median_price >= input$price_range[1]
                                & all_timeseries$median_price <= input$price_range[2], ]
      
      selected$norm_price = selected$median_price / max(selected$median_price)
      selected$norm_rent = selected$median_rent / max(selected$median_rent)
      
      closest_price_rent <- function(e) {
        if(is.null(e)) return("NULL\n\n")
        distance = abs(e$x / max(selected$median_price) - selected$norm_price) + abs(e$y / max(selected$median_rent) - selected$norm_rent)
        idx = which.min(distance)
        paste0("\n location = ", selected$zip_code[idx], ", ", selected$state[idx], 
               ", price = ", selected$median_price[idx], 
               ", rent = ", selected$median_rent[idx], "\n\n")
      }
      
      paste0(
        "click: ", closest_price_rent(input$plot_click),
        "hover: ", closest_price_rent(input$plot_hover)
      )
    })
    
    output$population_yield <- renderPlot({
      selected = all_timeseries[all_timeseries$year_month == input$year_month 
                                & all_timeseries$median_price >= input$price_range[1]
                                & all_timeseries$median_price <= input$price_range[2], ]
      top_index = min(input$top_max_num_entries, dim(selected)[1] * input$top_percentage)
      
      # myan: do an inner join
      merged_results = merge(selected[1:top_index, ], all_population, by.x = "zip_code", by.y = "zip_code")
      merged_results$group = "Other"
      if (input$selected_zipcodes != "all")
      {
        selected_zipcodes = rapply(list(strsplit(input$selected_zipcodes, ",")[[1]]), as.numeric)
        merged_results$group[is.element(merged_results$zip_code, selected_zipcodes)] = "Selected"
      }
      qplot(closest_city_population, gross_yield, data = merged_results, 
            colour=factor(group), 
            size=I(5), 
            main = "Population vs. Gross Yield",
            xlab = "Log population of closest city",
            ylab = "Annualized gross rental return (%)",
            log = "x") 
    })
    
    output$population_info <- renderText({
      selected = all_timeseries[all_timeseries$year_month == input$year_month 
                                & all_timeseries$median_price >= input$price_range[1]
                                & all_timeseries$median_price <= input$price_range[2], ]
      top_index = min(input$top_max_num_entries, dim(selected)[1] * input$top_percentage)
      # myan: do an inner join
      merged_results = merge(selected[1:top_index, ], all_population, by.x = "zip_code", by.y = "zip_code")
      
      closest_population <- function(e) {
        if(is.null(e)) return("NULL\n\n")
        valid_x = e$x >= 0.95 * merged_results$closest_city_population & e$x <= 1.05 * merged_results$closest_city_population
        valid_y = e$y >= merged_results$gross_yield - 1 & e$y <= merged_results$gross_yield + 1
        valid = valid_x & valid_y
        if(!any(valid)) return ("NULL\n\n")
        
        valid_results = merged_results[valid, ]
        distance = (e$x / valid_results$closest_city_population - 1) ^ 2 + (e$y / valid_results$gross_yield - 1) ^ 2
        idx = which.min(distance)
        paste0("\n location = ", valid_results$zip_code[idx], ", ", valid_results$state.x[idx], 
               "\n closest_city = ", valid_results$closest_city[idx], 
               "\n closest_city_population = ", valid_results$closest_city_population[idx],
               "\n price = ", valid_results$median_price[idx], ", rent = ", valid_results$median_rent[idx], "\n\n")
      }
      
      paste0(
        "click: ", closest_population(input$plot_click),
        "hover: ", closest_population(input$plot_hover)
      )
    })
    
    output$school_yield <- renderPlot({
      selected = all_timeseries[all_timeseries$year_month == input$year_month 
                                & all_timeseries$median_price >= input$price_range[1]
                                & all_timeseries$median_price <= input$price_range[2], ]
      top_index = min(input$top_max_num_entries, dim(selected)[1] * input$top_percentage)
      
      # myan: do an inner join
      yield_gsrating = merge(selected[1:top_index, ], zip_code_rating, by.x = "zip_code", by.y = "zip_code")
      yield_gsrating$group = "Other"
      if (input$selected_zipcodes != "all")
      {
        selected_zipcodes = rapply(list(strsplit(input$selected_zipcodes, ",")[[1]]), as.numeric)
        yield_gsrating$group[is.element(yield_gsrating$zip_code, selected_zipcodes)] = "Selected"
      }
      
      qplot(avg_gsrating, gross_yield, data = yield_gsrating, 
            colour=factor(group), 
            size=I(5), 
            main = "Avg School Rating vs. Gross Yield",
            xlab = "Average school rating for the area",
            ylab = "Annualized gross rental return (%)")
    })
    
    output$school_info <- renderText({
      selected = all_timeseries[all_timeseries$year_month == input$year_month 
                                & all_timeseries$median_price >= input$price_range[1]
                                & all_timeseries$median_price <= input$price_range[2], ]
      top_index = min(input$top_max_num_entries, dim(selected)[1] * input$top_percentage)
      
      # myan: do an inner join
      yield_gsrating = merge(selected[1:top_index, ], zip_code_rating, by.x = "zip_code", by.y = "zip_code")
      
      closest_school <- function(e) {
        if(is.null(e)) return("NULL\n\n")
        valid_x = e$x >= yield_gsrating$avg_gsrating - 0.5 & e$x <= yield_gsrating$avg_gsrating + 0.5
        valid_y = e$y >= yield_gsrating$gross_yield - 1 & e$y <= yield_gsrating$gross_yield + 1
        valid = valid_x & valid_y
        if(!any(valid)) return ("NULL\n\n")
        
        valid_results = yield_gsrating[valid, ]
        distance = (e$x / valid_results$avg_gsrating - 1) ^ 2 + (e$y / valid_results$gross_yield - 1) ^ 2
        idx = which.min(distance)
        paste0("\n location = ", valid_results$zip_code[idx], ", ", valid_results$state.x[idx], 
               "\n average_school_rating = ", valid_results$avg_gsrating[idx],
               "\n price = ", valid_results$median_price[idx], ", rent = ", valid_results$median_rent[idx], "\n\n")
      }
      
      paste0(
        "click: ", closest_school(input$plot_click),
        "hover: ", closest_school(input$plot_hover)
      )
    })
    
    drawdown_percent <- function(x) {
      drawdown = 0
      for (i in 1:length(x))
      {
        drawdown = max(drawdown, (max(x[1:i]) - x[i]) / max(x[1:i]))
      }
      return(round(drawdown * 100, digits = 2))
    }
    
    drawdown_dollar <- function(x) {
      drawdown = 0
      for (i in 1:length(x))
      {
        drawdown = max(drawdown, (max(x[1:i]) - x[i]))
      }
      return(drawdown)
    }
    
    output$price_variability <- renderPlot({
      selected = all_timeseries[all_timeseries$year_month == input$year_month 
                                & all_timeseries$median_price >= input$price_range[1]
                                & all_timeseries$median_price <= input$price_range[2], ]
      top_index = min(input$top_max_num_entries, dim(selected)[1] * input$top_percentage)
      top_zipcodes_all_time = all_timeseries[is.element(all_timeseries$zip_code, selected$zip_code[1:top_index]), ]
      
      if (input$drawdown_mode == "Dollar")
      {
        drawdown = aggregate(top_zipcodes_all_time$median_price, list(zip_code=top_zipcodes_all_time$zip_code), drawdown_dollar)
      }
      else
      {
        drawdown = aggregate(top_zipcodes_all_time$median_price, list(zip_code=top_zipcodes_all_time$zip_code), drawdown_percent) 
      }
      drawdown = rename(drawdown, c("x"="drawdown"))
      drawdown = drawdown[order(drawdown$drawdown), ]
      
      top_zipcodes_all_time = merge(top_zipcodes_all_time, drawdown, by.x = "zip_code", by.y = "zip_code")
      
      top_zipcodes_all_time$group = "Other"
      if (input$selected_zipcodes != "all")
      {
        selected_zipcodes = rapply(list(strsplit(input$selected_zipcodes, ",")[[1]]), as.numeric)
        top_zipcodes_all_time$group[is.element(top_zipcodes_all_time$zip_code, selected_zipcodes)] = "Selected"
      }
      
      ggplot(top_zipcodes_all_time, aes(x = reorder(zip_code, drawdown), y = median_price, fill=group)) + 
        geom_boxplot() + 
        xlab("Top Zipcodes - Ordered by Price Variability") + 
        ylab("Median Price Variability") + 
        theme(axis.text.x = element_text(angle = 90, hjust = 0))
    })
    
    output$price_variability_info <- renderText({
      selected = all_timeseries[all_timeseries$year_month == input$year_month 
                                & all_timeseries$median_price >= input$price_range[1]
                                & all_timeseries$median_price <= input$price_range[2], ]
      top_index = min(input$top_max_num_entries, dim(selected)[1] * input$top_percentage)
      top_zipcodes_all_time = all_timeseries[is.element(all_timeseries$zip_code, selected$zip_code[1:top_index]), ]
      
      if (input$drawdown_mode == "Dollar")
      {
        drawdown = aggregate(top_zipcodes_all_time$median_price, list(zip_code=top_zipcodes_all_time$zip_code), drawdown_dollar)
      }
      else
      {
        drawdown = aggregate(top_zipcodes_all_time$median_price, list(zip_code=top_zipcodes_all_time$zip_code), drawdown_percent) 
      }
      drawdown = rename(drawdown, c("x"="drawdown"))
      drawdown = drawdown[order(drawdown$drawdown), ]
      
      top_zipcodes_all_time = merge(top_zipcodes_all_time, drawdown, by.x = "zip_code", by.y = "zip_code")
      
      closest_school <- function(e) {
        if(is.null(e)) return("NULL\n\n")
        
        round_x = round(e$x)
        nearest_zipcode = drawdown$zip_code[round_x]
        is_selected_zip_code = top_zipcodes_all_time$zip_code == nearest_zipcode
        
        if (input$drawdown_mode == "Percentage")
        {
          suffix = "%"
        }
        else
        {
          suffix = ""
        }
        
        paste0("\n location = ", top_zipcodes_all_time$zip_code[is_selected_zip_code][1], ", ", top_zipcodes_all_time$state[is_selected_zip_code][1], 
               "\n max_price = ", max(top_zipcodes_all_time$median_price[is_selected_zip_code]),
               "\n min_price = ", min(top_zipcodes_all_time$median_price[is_selected_zip_code]), 
               "\n median_price = ", median(top_zipcodes_all_time$median_price[is_selected_zip_code]), 
               "\n max_drawdown = ", top_zipcodes_all_time$drawdown[is_selected_zip_code][1], suffix, "\n\n")
      }
      
      paste0(
        "click: ", closest_school(input$plot_click),
        "hover: ", closest_school(input$plot_hover)
      )
    })
  }
)