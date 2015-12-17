library(shiny)

# ui.R
shinyUI(
  fluidPage(
    titlePanel("Intelli Invest"),
  
    sidebarLayout(
      sidebarPanel(
        p("This is a demo of Intelli Invest. Due to server limitations, the data is limited to between 201401 and 201510"),
        p("You may add zip codes to the text box 'Selected zipcodes' below and they will be highlighted in different colors in other tabs."),
      
      sliderInput("price_range", 
                  label = "Median Price Range:",
                  min = 0, max = 2000000, value = c(0, 2000000)),
      
      numericInput("year_month", label = "Select Year_Month:", value = 201510),
      
      numericInput("top_percentage", label = "Fraction of top return zip codes:", value = 0.25),
      
      numericInput("top_max_num_entries", label = "Maximun Number of Entries in Top Group: ", value = 25),
      
      textInput("selected_zipcodes", label = "Selected zipcodes for further investigation: ", value = "all"),
      
      selectInput("drawdown_mode", label = "Select drawdown mode", 
                  choices = list("Dollar", "Percentage"), selected = "Dollar")
    ),
    
    
    mainPanel(
      tabsetPanel(
        tabPanel("Price vs. Rent Overview", 
                 p("This chart explores the dyanmics of median monthly rent and median purchase price for all zip codes in a given month within a certain
                   price range. \n\n
                   We split the top x% or a maximum of y (both x and y definable on the left) into the 'Top' group and also fit a simple linear 
                   regression to show the rental return differences between the two groups."), 
                 plotOutput("price_rent", click = "plot_click", hover = "plot_hover"), 
                 verbatimTextOutput("price_rent_info")),
        tabPanel("Population - Top", 
                 p("This chart plots the population of closest major city for all the 'Top' zip codes. \n
                   A major city is defined as where population is more than 100,000. \n
                   Close is defined as the distance between two places is less than 80 kilometers."),
                 plotOutput("population_yield", click = "plot_click", hover = "plot_hover"), 
                 verbatimTextOutput("population_info")),
        tabPanel("School Ratings - Top", 
                 p("This chart explores the average school rating versus the rental return for all the 'Top' zip codes. \n
                   School rating is an arithmetic average of 20 schools within 5 miles radius of a zip code, retrieved from GreatSchools.org API."),
                 plotOutput("school_yield", click = "plot_click", hover = "plot_hover"), 
                 verbatimTextOutput("school_info")),
        tabPanel("Price Variability - Top", 
                 p("This chart explores the price variability of all the 'Top' zip codes. Intuitively, one wants to invest in places where the median prices either
                   grows consistently or stablizes during less favorable market conditions. \n\n
                   We therefore compute both the absolute drawdown and drawdown as a percentage, and rank the zip codes from the most stable to the least"),
                 plotOutput("price_variability", click = "plot_click", hover = "plot_hover"), 
                 verbatimTextOutput("price_variability_info"))
        )
      )
    
    )
  )
)