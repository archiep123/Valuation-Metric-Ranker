from yfinance import Ticker, download
from pandas import ExcelWriter
from sys import exit
try:
    from os import startfile
except ImportError:
    startfile=None
from math import isfinite

#determine whether or not user wants to use the program after explaining what it does
def start_program():
    #brief program explanation
    print("""
Hello. The following program uses inverted min-max normalisation to rank a predefined list of large-cap and mega-cap technology companies based on seven common valuation metrics before displaying the ranking results to the user. The first ranking displayed by the program will show which companies have the
lowest valuation metric values across the seven valuation metrics when all seven metrics are weighted equally. The second ranking displayed by the program will show which companies have the lowest valuation metric values when the weighting is adjusted to reduce bias against younger, high-growth companies.
The program will then ask the user whether they would like to view a line graph showing the 50-day moving average (50DMA), 200-day moving average (200DMA), and adjusted closing price over the past trading year for any of the ranked companies. If the user chooses to do so, the program will automatically
open an Excel file with an active sheet containing the line graph for the company specified by the user.""")

    #determine if the user wants to use the program or not
    user_choice_to_start_program=input("\nYou have now been informed of the function of this program. Would you like to proceed (Y/N)? ").strip().upper() 

    #input validation
    valid_choices={"Y", "N"}
    while user_choice_to_start_program not in valid_choices:
        user_choice_to_start_program=input("\nError. Please ensure you are only inputting a 'Y' or an 'N'. Try again: ").strip().upper() 

    # if they dont, exit program. If they do, program proceeds
    if user_choice_to_start_program=="N": 
        exit()


#display each of the two rankings. If the rankings create subsequent user interest in a particular company, display a line graph showing the adjusted closing price, 50DMA and 200DMA over the past year for this company in excel
def display_results(both_weighting_final_scores, stock_tickers):

    #call the function that displays the overall stock ranking for each valuation metric weighting 
    calculate_ranking(both_weighting_final_scores, stock_tickers)

    #determine whether or not user is interested in a company and would like to see a line graph for it
    user_choice=input("Given these results, you may want to investigate one of the companies ranked by the program further. To kickstart your subsequent research, this program has the ability to display in excel a line graph showing the adjusted closing price, the 50DMA and the 200DMA over the past trading year for the company you are interested in. If you would like the program to do this, please enter the ticker for the company displayed in the rankings that you are interested in. Otherwise, please enter 'E'.").strip().upper()

    #input validation
    while user_choice not in stock_tickers:
        if user_choice=='E':
           exit()
        user_choice=input("\nError. Please ensure you have entered the ticker symbol for a company in the rankings provided or 'E'. Try again: ").strip().upper() 

    #create a dataframe with the adjusted closing prices for the user's chosen company over the past 2 years. Add columns to this dataframe that contain the 50DMA and the 200DMA at each trading day over the past two years that there is enough prior adjusted closing prices for their calculation. Cut down the
    #dataframe so it only stores data for the last trading year
    data_for_chosen_stock=download(user_choice, period="2y")[['Close']]
    data_for_chosen_stock["50DMA"]=data_for_chosen_stock['Close'].rolling(50).mean()
    data_for_chosen_stock["200DMA"]=data_for_chosen_stock['Close'].rolling(200).mean()
    data_for_chosen_stock=data_for_chosen_stock.tail(252)
                    
    #create an excel file called 'results.xlsx' that has a sheet called 'Data Sheet' with the data from data_for_chosen_stock and a sheet called 'Results' that is set as the active sheet.
    with ExcelWriter("results.xlsx", engine="xlsxwriter") as writer:
        data_for_chosen_stock.to_excel(writer, sheet_name="Data Sheet")
        workbook=writer.book
        workbook.add_worksheet("Results") 
        writer.sheets['Results'].activate()

        #create a line graph that displays the adjusted closing price, 50DMA and 200DMA over the last trading year for the user's chosen company, add it to the 'Results' sheet and open the 'results.xlsx' file. The file-opening feature will only work on Windows operating systems. Otherwise, the file must be opened
        #manually.
        data_sheet_final_data_row_number=len(data_for_chosen_stock)+2
        chart=workbook.add_chart({'type':'line'})
        for index, (level_0_column_header, _) in enumerate(data_for_chosen_stock.columns, start=1):
            chart.add_series({'name':f'{level_0_column_header}', 'categories':['Data Sheet', 3, 0, data_sheet_final_data_row_number, 0], 'values':['Data Sheet', 3, index, data_sheet_final_data_row_number, index]})                 
        chart.set_x_axis({'name': 'Date and Time', 'name_font':{'size':15}, 'num_font':{'size':11}, 'major_gridlines': {'visible':True}, 'minor_gridlines': {'visible':True}}) 
        chart.set_y_axis({'name':'Price ($)', 'name_font':{'size':15}, 'num_font':{'size':11}, 'major_gridlines': {'visible':True}, 'minor_gridlines': {'visible':True}}) 
        chart.set_size({'width':1500, 'height':1000}) 
        chart.set_title({'name': f"50DMA, 200DMA and Closing Price (adj) Over Past Year for {user_choice}"}) 
        writer.sheets["Results"].insert_chart('A1', chart)
        if startfile:
            startfile('results.xlsx')
        else:
            print(f"\nresults.xlsx has been created. Please open it manually to view the chart.")
        



















#Get the metric values for all valid stock tickers across each valuation metric analysed by the program.  Get the total scores for each stock across both of the valuation metric weightings
def calculate_total_stock_scores(stock_tickers_without_filtering):
    
    #returns a dictionary of lists with the metric values for all valid stocks across each valuation metric used by the program as well as a list of all the valid stock tickers
    all_values_for_each_metric, stock_tickers=retrieve_stock_information(stock_tickers_without_filtering)

    #initialises the totals for each of the two valuation metric weightings
    number_of_stocks=len(stock_tickers)
    balanced_weighting_valuation_score, growth_adjusted_valuation_score=[0]*number_of_stocks, [0]*number_of_stocks

    #defines the proportions used in the two different valuation metric weightings. Storing these calculations as variables means they only have to be solved once independent of the number of times they are used. 
    one_seventh=1/7
    three_twenty_fifths=3/25
    one_fifth=1/5
    
    #create a tuple that will be used to automate the process of calling each scoring function and incrementing the total score for each stock. The tuple at position zero in the outer tuple is used to get the total scores when the valuation metric weighting is balanced and the tuple at position 1 is used to get
    #the total scores when the valuation metric weighting is adjusted to reduce bias against young, growing companies
    score_calculation_data = ( 
        (
            (score_for_pe,
             (balanced_weighting_valuation_score, (all_values_for_each_metric['trailingPE'], all_values_for_each_metric['forwardPE']), one_seventh)),

            (score_for_price_to_fcf,
             (balanced_weighting_valuation_score, all_values_for_each_metric['marketCap'], all_values_for_each_metric['freeCashflow'],one_seventh)),

            (score_for_peg,
             (balanced_weighting_valuation_score, all_values_for_each_metric['trailingPegRatio'], all_values_for_each_metric['trailingPE'], one_seventh)),

            (score_for_ev_to_ebitda,
             (balanced_weighting_valuation_score, all_values_for_each_metric['enterpriseValue'], all_values_for_each_metric['ebitda'], all_values_for_each_metric['enterpriseToEbitda'], one_seventh)),

            (score_for_ps,
             (balanced_weighting_valuation_score, all_values_for_each_metric['priceToSalesTrailing12Months'], one_seventh)),

            (score_for_ev_to_revenue,
             (balanced_weighting_valuation_score, all_values_for_each_metric['enterpriseToRevenue'], all_values_for_each_metric['enterpriseValue'], one_seventh)),
        ),
        
        (
            (score_for_pe,
             (growth_adjusted_valuation_score, (all_values_for_each_metric['trailingPE'], all_values_for_each_metric['forwardPE']), three_twenty_fifths)),

            (score_for_price_to_fcf,
             (growth_adjusted_valuation_score, all_values_for_each_metric['marketCap'], all_values_for_each_metric['freeCashflow'],  three_twenty_fifths)),

            (score_for_peg,
             (growth_adjusted_valuation_score, all_values_for_each_metric['trailingPegRatio'],  all_values_for_each_metric['trailingPE'], three_twenty_fifths)),

            (score_for_ev_to_ebitda,
             (growth_adjusted_valuation_score, all_values_for_each_metric['enterpriseValue'], all_values_for_each_metric['ebitda'], all_values_for_each_metric['enterpriseToEbitda'], three_twenty_fifths)),

            (score_for_ps,
             (growth_adjusted_valuation_score, all_values_for_each_metric['priceToSalesTrailing12Months'], one_fifth)),

            (score_for_ev_to_revenue,
             (growth_adjusted_valuation_score, all_values_for_each_metric['enterpriseToRevenue'], all_values_for_each_metric['enterpriseValue'], one_fifth)),
        )
    )
    
    #iterate for each of the two valuation metric weightings
    for valuation_metric_weighting in score_calculation_data:
        
        #for the current valuation metric weighting, this inner loop automates the process of calling the scoring functions and updating the total score for each stock across all the valuation metrics analysed by the program. 
        for function_name, args in valuation_metric_weighting:
            function_name(*args)
    
    return balanced_weighting_valuation_score, growth_adjusted_valuation_score, stock_tickers


#determine which stocks have valid values for all the metrics analysed by the program and store the metric values for these stocks
def retrieve_stock_information(stock_tickers_without_filtering):

    # create a tuple of all the metrics that are analysed by the program
    all_metrics_used_by_program=(
        'ebitda',
        'enterpriseValue',
        'trailingPE',
        'forwardPE',
        'priceToSalesTrailing12Months',
        'enterpriseToRevenue',
        'enterpriseToEbitda',
        'trailingPegRatio',
        'marketCap',
        'freeCashflow',
    )
    
    stock_tickers=[]
    all_values_for_each_metric={metric: [] for metric in all_metrics_used_by_program}        

    #for each stock in the unfiltered list, check whether its information dictionary can be retrieved and check that the information dictionary stores a finite numerical value for each metric used by the program
    for stock_ticker in stock_tickers_without_filtering: 
        try:
            #validation 1: the stock's information dictionary can be retrieved
            stock_ticker_info=Ticker(stock_ticker).info 

            #validation 2: the information dictionary stores a finite numerical value for each metric used by the program
            if not all(isfinite(stock_ticker_info.get(metric)) for metric in all_metrics_used_by_program):
                print(f"\n{stock_ticker} will not be considered by the program because it failed the validations required for the program to be able to analyse it.")
                continue
            
            #once stock has been validated, add its metric values to the corresponding lists in the all_values_for_each_metric dictionary
            for metric, metric_values_for_each_stock in all_values_for_each_metric.items():
                metric_values_for_each_stock.append(stock_ticker_info[metric])

            #once stock has been validated, add its ticker to the filtered list of stock tickers that will be analysed by the program
            stock_tickers.append(stock_ticker)

        #any error occurring during data retrieval or data checking is assumed to be a result of the stock failing the validations. Consequently, when an error is raised, the corresponding stock is not added to the filtered list of stocks analysed by the program
        except Exception: 
            print(f"\n{stock_ticker} will not be considered by the program because it failed the validations required for the program to be able to analyse it.") 

    #if removing the invalid stocks leaves less than five remaining, exit program
    if len(stock_tickers)<5: 
        print("\nError. Since too many of the stocks didnt pass both of the validations necessary to be analysed by the program, it cannot fulfill its function and will now end.")
        exit()
    
    #otherwise, return a dictionary of lists that stores all of the metric values for the valid stocks across each metric analysed by the program as well as a list of the valid stock tickers
    return all_values_for_each_metric, stock_tickers


#update the total score so far for each stock whose total is being updated using min-max normalisation. Inverting the min-max normalisation is necessary to create an inverse relationship between each company's valuation metric value and the score it is awarded.
def assign_scores_to_stocks(accumulating_score_for_valuation_metric_weighting, all_stock_metric_values, weighting, indices_for_total_update=None):
    
    #find the number of stocks whose total score so far is being updated using min-max normalisation
    num_valid_stocks=len(all_stock_metric_values)
            
    #This condition requires there to be at least 2 stocks whose totals are being updated using min-max normalisation before the normalisation is used. This is relevant for all the scoring functions except 'score_for_ps' where there are other ways for totals to be updated. When scoring these functions,
    #the number of metric values being normalised can range from zero to the number of valid stocks. As long as this number exceeds one, normalisation can be applied. If it equals one, separate treatment is required and, if it equals zero, no normalisation occurs.
    if num_valid_stocks>1:

        #This condition applies to 'score_for_ps'. In this function, min-max normalisation is the only method used to update totals and so every stock has its P/S value normalised. Therefore, it would be unnecessary for this function to store the index of each stock whose
        #P/S value is being normalised. Consequently, this function doesnt provide an argument for 'indices_for_total_update', meaning that when the P/S values are being scored, 'indices_for_total_update' takes its default value of None. When this occurs, 'indices_for_total_update' is set to a
        #range object covering all valid stock indices.
        if indices_for_total_update is None: 
            indices_for_total_update=range(num_valid_stocks)

        #get the maximum and minimum metric values using a single pass through the data
        max_metric_value_across_stocks, min_metric_value_across_stocks=float('-inf'),float('inf')
        for metric_value in all_stock_metric_values:
            if metric_value<min_metric_value_across_stocks:
                min_metric_value_across_stocks=metric_value
            if metric_value>max_metric_value_across_stocks:
                max_metric_value_across_stocks=metric_value
        
        #get the difference between the maximum and minimum metric values
        normalisation_range=max_metric_value_across_stocks-min_metric_value_across_stocks

        #for any valuation metric, if the normalisation range is zero then every stock being scored has the same valuation metric value and min-max normalisation cannot be applied because division by zero will occur. Thus, no totals are updated for this valuation metric.
        if normalisation_range==0:
            return
        
        #Invert the normalised scores and add them to the totals. The weighting variable scales each valuation metric's normalised score so that it contributes the desired proportion of the total score.
        for index, stock_metric_value in zip(indices_for_total_update, all_stock_metric_values):
                accumulating_score_for_valuation_metric_weighting[index]+=(1-(stock_metric_value-min_metric_value_across_stocks)/normalisation_range)*weighting
        
   #if only one stock is being scored using normalisation, min-max normalisation cannot be applied because the normalisation range would be zero. Therefore, the stock's total is manually incremented by 0.5 points instead. Note: whenever 'indices_for_total_update' is None, 'num_valid_stocks' is equal to the total number
    #of stocks being analysed by the program and 'retrieve_stock_information' forces this total to be >=5. Thus, 'elif num_valid_stocks == 1' will never execute when indices_for_total_update is None.
    elif num_valid_stocks == 1:
        accumulating_score_for_valuation_metric_weighting[indices_for_total_update[0]]+=(0.5*weighting)   
            

#update the total for each stock based on its P/S. Since P and S can both be assumed non-negative, all the P/S values can be scored using inverted min-max normalisation, making this function the most elementary case of valuation metric scoring.
def score_for_ps(accumulating_score_for_valuation_metric_weighting, trailing_ps_values, weighting):

    #call the function that uses inverted min-max normalisation to update the total for each stock based on its P/S 
    assign_scores_to_stocks(accumulating_score_for_valuation_metric_weighting, trailing_ps_values, weighting)


#update the total for each stock based on its P/E. 
def score_for_pe(accumulating_score_for_valuation_metric_weighting, pe_metrics_to_be_scored_on, weighting):

    #The outer for loop iterates for the forward P/E and trailing P/E. The inner for loop creates a filtered list of the P/E values for the stocks whose earnings are positive and a list of the positions of these stocks in the unfiltered P/E list. 
    for pe_metric in pe_metrics_to_be_scored_on:
        indices_for_total_update, pe_metric_values=[], []
        for index, pe_value in enumerate(pe_metric):
            if pe_value>0:
                indices_for_total_update.append(index)
                pe_metric_values.append(pe_value)

        #call the function that uses inverted min-max normalisation to update the total for each stock with a positive P/E value. Stocks with a non-positive P/E value dont have their totals updated because their data isnt passed into 'assign_scores_to_stocks'
        assign_scores_to_stocks(accumulating_score_for_valuation_metric_weighting, pe_metric_values, weighting, indices_for_total_update)


#update the total for each stock based on its P/EG. 
def score_for_peg(accumulating_score_for_valuation_metric_weighting, trailing_peg_values, trailing_pe_values, weighting):

    #create a filtered list of the P/EG values for the stocks whose P/EG and P/E values are both positive. Also, create a list of the positions of these stocks in the unfiltered P/E and P/EG lists.
    peg_values_for_normalisation, peg_indices_for_normalisation=[], []
    for index, (trailing_peg, trailing_pe) in enumerate(zip(trailing_peg_values, trailing_pe_values)):
        if trailing_pe>0 and trailing_peg>0:
            peg_values_for_normalisation.append(trailing_peg)
            peg_indices_for_normalisation.append(index)

    #call the function that uses inverted min-max normalisation to update the total for each stock whose P/EG and P/E values are both positive. Stocks that have a negative P/E and negative P/EG, negative P/E and positive P/EG, or positive P/E and negative P/EG dont have their totals updated because their data isnt passed
    #into 'assign_scores_to_stocks'
    assign_scores_to_stocks(accumulating_score_for_valuation_metric_weighting, peg_values_for_normalisation, weighting, peg_indices_for_normalisation)


#update the total for each stock based on its EV/R
def score_for_ev_to_revenue(accumulating_score_for_valuation_metric_weighting, ev_to_revenue_values, ev_values, weighting):

    #create a filtered list of the EV/R values for the stocks whose EV values are non-negative. Also, create a list of the positions of these stocks in the unfiltered EV/R list. Stocks whose EV values are negative don't have their totals updated using inverted min-max normalisation. Instead, their totals are
    #manually incremented by one point. 
    ev_to_revenue_values_for_normalisation, ev_to_revenue_indices_for_normalisation=[], []
    for index, ev_value in enumerate(ev_values):
        if ev_value>=0:
            ev_to_revenue_values_for_normalisation.append(ev_to_revenue_values[index])
            ev_to_revenue_indices_for_normalisation.append(index)
        else:
            accumulating_score_for_valuation_metric_weighting[index]+=(1*weighting)

    #call the function that uses inverted min-max normalisation to update the total for each stock whose EV value is non-negative. 
    assign_scores_to_stocks(accumulating_score_for_valuation_metric_weighting, ev_to_revenue_values_for_normalisation, weighting, ev_to_revenue_indices_for_normalisation)


#update the total for each stock based on its EV/EBITDA 
def score_for_ev_to_ebitda(accumulating_score_for_valuation_metric_weighting, ev_values, ebitda_values, ev_to_ebitda_values, weighting):

    #create a filtered list of the EV/EBITDA values for the stocks with positive EV and positive EBITDA or zero EV. Also, create a list of the positions of these stocks in the unfiltered EV and EBITDA lists. Stocks with negative EV and positive EBITDA or negative EV and negative EBITDA do not have their totals
    #updated using inverted min-max normalisation. Instead, those with negative EV and positive EBITDA have their totals manually incremented by one point, and those with negative EV and negative EBITDA have their totals manually incremented by 0.5 points.
    ev_to_ebitda_values_for_normalisation, ev_to_ebitda_indices_for_normalisation=[], []
    for index, (ev_value, ebitda_value) in enumerate(zip(ev_values, ebitda_values)):
        if ebitda_value>0:
            if ev_value>=0:
                ev_to_ebitda_values_for_normalisation.append(ev_to_ebitda_values[index])
                ev_to_ebitda_indices_for_normalisation.append(index)
            else:
                accumulating_score_for_valuation_metric_weighting[index]+=(1*weighting)
        else:
            if ev_value==0:
                ev_to_ebitda_values_for_normalisation.append(ev_to_ebitda_values[index])
                ev_to_ebitda_indices_for_normalisation.append(index)
            elif ev_value<0:
                accumulating_score_for_valuation_metric_weighting[index]+=(0.5*weighting)
            
    #call the function that uses inverted min-max normalisation to update the total for each stock with positive EV and positive EBITDA or zero EV. Stocks that have a negative EBITDA and positive EV dont have their totals updated because their data isnt passed into 'assign_scores_to_stocks' and their totals arent
    #manually incremented in the for loop 
    assign_scores_to_stocks(accumulating_score_for_valuation_metric_weighting, ev_to_ebitda_values_for_normalisation, weighting, ev_to_ebitda_indices_for_normalisation)


#update the total for each stock based on its P/FCF. This function is similar to score_for_pe() with the addition of calculating the ratios as well as updating the totals using them
def score_for_price_to_fcf(accumulating_score_for_valuation_metric_weighting, market_cap_values, free_cash_flow_values, weighting):

    #create a list of the P/FCF values for the stocks whose FCF values are positive. Also, create a list of the positions of these stocks in the unfiltered market capitalisation and FCF lists.
    price_to_fcf_values_for_normalisation, price_to_fcf_indices_for_normalisation=[], []
    for index, (market_cap_value, free_cash_flow_value) in enumerate(zip(market_cap_values, free_cash_flow_values)):
        if free_cash_flow_value>0:
            price_to_fcf_values_for_normalisation.append(market_cap_value/free_cash_flow_value)
            price_to_fcf_indices_for_normalisation.append(index)

    #call the function that uses inverted min-max normalisation to update the total for each stock whose FCF value is positive. Stocks with non-positive FCF values dont have their totals updated because their data isnt passed into 'assign_scores_to_stocks'
    assign_scores_to_stocks(accumulating_score_for_valuation_metric_weighting, price_to_fcf_values_for_normalisation, weighting, price_to_fcf_indices_for_normalisation)


#for each valuation metric weighting, get and display the 1224 ranking based on the final scores 
def calculate_ranking(both_weighting_final_scores, stock_tickers):
    
    #used to state the valuation metric weighting that the ranking corresponds to. This tuple is ordered to match the scores in both_weighting_final_scores
    weightings=('balanced', 'growth-adjusted')

    # loop for each of the two valuation metric weightings
    for weighting, individual_weighting_final_scores in zip(weightings, both_weighting_final_scores):
        #round each final stock score for the given weighting to 4dp and create a list of (rounded score, stock ticker) tuples that is sorted in descending order
        ordered_scores=sorted(
            ((round(stock_score, 4), stock_ticker) for stock_score, stock_ticker in zip(individual_weighting_final_scores, stock_tickers)),
            key=lambda x: x[0],
            reverse=True
        )

        #begin creating the output by stating the weighting that this ranking relates to and setting the stock with the highest score to be ranked number one
        rank=1
        message=[f"\nThe program's ranking of companies based on their valuation metric values when the {weighting} valuation metric weighting is used is:\n{rank}. {ordered_scores[0][1]}"] 

        #determine the rank for the rest of the stocks and add them to the output generated so far. This logic applies 1224 ranking in the event of a draw
        for i in range(1, len(ordered_scores)):
            current_score, current_name = ordered_scores[i]
            previous_score, _ = ordered_scores[i-1]
            if current_score!=previous_score:
                rank=i+1
            message.append(f'{rank}. {current_name}')

        # display the stock ranking for the given approach
        print("\n".join(message)+'\n') 

#main
stock_tickers_without_filtering=["AAPL","MSFT","NVDA","INTC","ORCL","AVGO","AMD","QCOM","TXN","ADBE",'CRM',"TSM","MU","NOW","ASML", 'ADSK']
start_program()
balanced_weighting_valuation_score, growth_adjusted_valuation_score, stock_tickers=calculate_total_stock_scores(stock_tickers_without_filtering)
display_results((balanced_weighting_valuation_score, growth_adjusted_valuation_score), stock_tickers)
