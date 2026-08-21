## **Introduction**

**Use**

When searching for undervalued companies, I had a wide range of valuation metrics at my disposal. However, rather than relying on any single measure, I wanted to identify companies that appeared inexpensive across multiple, independent valuation metrics. This is because using a broader set of metrics reduces the risk that the result is driven by the quirks of any one measure.

The program detailed below was designed to help achieve this. It ranks a predefined list of large-cap and mega-cap technology companies according to seven common valuation metrics, assigning higher rankings to companies with lower values across the metrics analysed. The purpose of this program is therefore not to determine which companies are definitively undervalued, but to provide a systematic way of identifying companies with low valuations so that further investigation can be completed.

It is important to recognise that a company with a low valuation can be a warning sign just as much as it can be an indication of undervaluation. There are many factors that can contribute to why a company might appear inexpensive, including the market expecting the company's earnings to decline and the company being in a financially distressed position.

Therefore, the user should be careful not to interpret the ranking outputted by the program as an ordering of companies from most to least undervalued. Instead, this program should be used as a tool to help sift for companies with relatively low valuations, after which users should conduct independent research into each high-ranking company's financial health, prospects, and current circumstances before determining whether its valuation represents a genuine opportunity.

**How it works**

By and large, the program calculates the score to award for each valuation metric by retrieving each company's value for the metric and applying inverted min-max normalisation to reward companies based on their relative performance. However, certain edge cases where peer comparison is not meaningful are handled via a manual point allocation. This means that each ranking displayed by the program should be interpreted as a combination of comparative and rule-based scoring instead of being purely based on relative performance.

## **Context**

**Data Source**

All valuation metric values are retrieved from Yahoo Finance using the yfinance Python library.

**Output**

The program outputs two separate rankings. The first displays the ranking of the companies when each of the seven valuation metrics contributes equally to the overall score. The second displays the ranking after the weighting is adjusted to put more emphasis on valuation metrics that are less biased against young, growing companies. The user is then given the option to view a line graph showing the 50DMA, 200DMA, and adjusted closing price over the past trading year for a company of their choice from the ranking tables.

Note: After the user inputs the company for which they would like to see a line graph, an Excel file with the graph displayed on the active sheet should automatically open. However, this feature is platform-dependent and implemented for Windows only.

## **Metric Weighting**

**The Reason for Two Separate Rankings**

Five of the seven valuation metrics analysed by the program use a benchmark for valuation that incorporates the company's profitability or cash generation. Consequently, equally weighting the valuation metrics may introduce a bias against companies that are young and expanding. Companies at this stage typically prioritise capturing market share over profitability and cost control, meaning they are more likely to have high valuation multiples when valuation is measured relative to earnings, EBITDA, or free cash flow.

By creating a second ranking that places greater emphasis on valuation multiples that measure valuation relative to the top line, the program can be used to support both value-investing and growth-investing approaches. The first ranking is more likely to favour established companies with stronger profitability and cash generation, making it more suitable for value investors. In contrast, the second ranking increases the likelihood of identifying high-growth companies by emphasising the focus on valuation relative to sales performance, making it more relevant to growth investors.

**Weighting Diagram**

- Balanced Valuation Score(100%)
  - Trailing P/E------------─┐
  - Forward P/E-------------┤
  - Price to Free Cash Flow-┤
  - Trailing P/EG------------┤---> (1/7 of Balanced Valuation Score)
  - EV / EBITDA-------------┤
  - Price to Sales------------┤
  - EV / Revenue------------┘

- Growth-Adjusted Valuation Score (100%)
  - Trailing P/E------------------------┐
  - Forward P/E-----------------------┤
  - Price to Free Cash Flow-----------┤---> (3/25 of Growth-Adjusted Valuation Score)
  - Trailing P/EG----------------------┤
  - EV / EBITDA-----------------------┘
  - Price to Sales------------------┐
  - EV / Revenue------------------┘-----> (1/5 of Growth-Adjusted Valuation Score)

## **Metric Insights**

**Metric Selection**

Certain valuation metrics analysed by the program may disproportionately benefit specific companies depending on their stage of progression and subsector. For example, an EBITDA-based valuation metric may favour capital-intensive companies such as TSMC by excluding D&A. This can be a significant expense for companies with large bases of depreciable or amortisable assets, leading to lower EV/EBITDA values.

However, it should be made clear that the valuation metrics analysed by the program are not intended to be unbiased across all companies. Instead, the program aims to use a broad enough range of valuation metrics to smooth out any resulting inequalities.

**Metric Justification**

Trailing P/E, Forward P/E:

Intention: reward companies trading at low valuations relative to their current and forecast earnings. This may seem counterintuitive because a low P/E can imply that the market has low expectations for future company growth. However, it is possible that a company has a low P/E because its growth has not yet been fully priced by the market.

Trailing P/EG:

Intention: reward companies trading at low valuations relative to their current earnings, adjusting for expected earnings growth. Assessing a company's P/EG ratio complements an assessment of its P/E. This is because the P/EG helps to separate a company whose P/E is low because the market expects weak or declining earnings growth from a company whose P/E is low despite expectations of strong future performance.

P/S, EV/R:

Intention: reward companies trading at low valuations relative to their total annual revenue. As discussed, valuation metrics that assess valuation relative to revenue provide an insight that isn't fully captured by those that use profitability or cash-flow measures as their valuation benchmark. By focussing on revenue, these metrics aren't influenced by the company's current cost structure and profitability, making them particularly useful when assessing companies invested heavily in growth.

Note: EV/R is used distinctly from P/S because it incorporates debt and cash positions to assess valuation in terms of the company's total value, rather than just the market value of equity.

EV/EBITDA:

Intention: reward companies whose enterprise value is low relative to their EBITDA. When calculating EBITDA, core operating costs such as SG&A and COGS are accounted for, but financing, taxation, and D&A are not. By not taking into account D&A and financing decisions, which have a less direct relationship with operating performance than SG&A and COGS, EBITDA can be used as a proxy for the profitability of a company's core operations. Therefore, EV/EBITDA can be viewed as an assessment of a company's valuation relative to a core operating profitability proxy. However, as previously alluded to, some individuals dispute the reliability of interpreting EBITDA in this way. This is because, given that D&A is not accounted for, differences in EV/EBITDA between companies can reflect a variation in the size of their depreciable or amortisable asset bases as much as differences in their operating profitability.

P/FCF:

Intention: reward companies trading at low valuations relative to their FCF. Unlike earnings-based metrics, FCF is derived directly from cash movements rather than accounting accruals, making it less susceptible to accounting manipulation. Additionally, unlike the EV/EBITDA, FCF accounts for capital expenditure. A company with a low P/FCF is inexpensively valued relative to the free cash it generates. This may indicate that the market has not fully priced the company's cash-generating ability, although it may also reflect expectations that its current level of free cash flow will decline.

## **Program Logic Comments**

Note: For the list of large-cap and mega-cap technology companies that the program analyses, most of the edge-case logic is unlikely to be triggered and is simply included for practice.

**Structure of Program**

The program is arranged to have functions that get user inputs and display results first. The functions used to calculate and compare the overall scores come next, separated by a large section of white space. The 'main' section at the end of the program defines the list of large-cap and mega-cap technology companies analysed by the program and makes the function calls required for the program to run.

**Why is Edge-Case Scoring Implemented?**

A valuation ratio will be correctly scored by inverted min-max normalisation when the numerator variables and denominator variables are both positive. In this case, inverted min-max normalisation will favour the ratio with the higher denominator when the numerator is constant, and will favour the ratio with the lower numerator when the denominator is constant.

A valuation ratio will also be correctly scored by inverted min-max normalisation when the numerator evaluates to zero and the denominator evaluates to a non-zero value. The ratio evaluates to zero, which is the minimum non-negative value, and, accordingly, will be awarded the maximum score. This fact — that a minimum value is given the maximum score — is exactly aligned with the intended rules followed by inverted min-max normalisation.

Of course, the case where the numerator is zero and the denominator is non-zero is degenerate because the ratio evaluates to zero independent of the denominator, so information regarding the magnitude of the denominator is lost. However, being a degenerate case doesn't mean that inverted min-max normalisation scores it incorrectly. The fact that the ratio evaluates to zero independent of the denominator's non-zero value is an inherent flaw of using ratios in general, but the value that the ratio evaluates to is still consistent with the score that it is awarded by inverted min-max normalisation. Therefore, this case does not require edge-case scoring because inverted min-max normalisation scores it consistently.

Edge-case scoring is only needed when either: A – inverted min-max normalisation can be used for scoring, but it leads to contradictory scoring, or B – inverted min-max normalisation cannot be used for scoring.

A occurs when any numerator and/or denominator variable becomes negative. This is because any variable turning negative causes its relationship with the valuation ratio to reverse from the relationship assumed by inverted min-max normalisation. In this project, there are five main cases for relationship reversal:

\- **There is one numerator variable and one denominator variable; the numerator variable is positive, and the denominator variable is negative.** In this case, as the numerator increases and the denominator is constant, the ratio decreases. This means that inverted min-max normalisation will favour the ratio with the higher numerator when the denominator is constant and negative. Of course, this contradicts what happens when the numerator and denominator are both positive. Valuation ratios like the P/E, where P can be assumed positive and E has the potential to be negative, fall under this case.

\- **There is one numerator variable and one denominator variable; the numerator variable is negative, and the denominator variable is positive.** In this case, as the numerator is constant and the denominator increases, the ratio increases. This means that inverted min-max normalisation will favour the ratio with the lower denominator when the numerator is constant and negative. Of course, this contradicts what happens when the numerator and denominator are both positive. Valuation ratios like the EV/R, where R can be assumed positive and EV has the potential to be negative, fall under this case.

\- **There is one numerator variable and two denominator variables; the numerator variable is positive, and the denominator variables are both negative.** In this case, as the numerator is constant and the two denominator variables increase, the ratio increases. This means that inverted min-max normalisation will favour the ratio with the lower respective denominator variables when the numerator is constant and positive. Of course, this contradicts what happens when the numerator and denominator variables are all positive. Valuation ratios like the P/EG, where P can be assumed positive and both E and G have the potential to be negative, fall under this case.

\- **There is one numerator variable and two denominator variables; the numerator variable and one denominator variable are positive, and the other denominator variable is negative.** In this case, as the numerator variable increases and the denominator variables are constant, the ratio decreases. Additionally, as the numerator variable and the negative denominator variable are constant and the positive denominator variable increases, the ratio increases. This means that inverted min-max normalisation will favour the ratio with the higher numerator variable when the denominator variables are constant, and will favour the ratio with the lower positive denominator variable when the negative denominator variable and the numerator variable are constant. Of course, these outcomes both contradict what happens when the numerator and denominator variables are all positive. Like the previous case, this applies to valuation ratios like the P/EG, where P can be assumed positive and both E and G can be positive or negative.

\- **There is one numerator variable and one denominator variable; the numerator variable is negative, and the denominator variable is negative too.** In this case, as the numerator is constant and the denominator increases, the ratio increases. Additionally, as the denominator is constant and the numerator increases, the ratio decreases. This means that inverted min-max normalisation will favour the ratio with the lower denominator when the numerator is constant and negative, and will favour the ratio with the higher numerator when the denominator is constant and negative. Of course, these outcomes both contradict what happens when the numerator and denominator are positive. Valuation ratios like the EV/EBITDA, where EV and EBITDA both have the potential to be negative, fall under this case.

B occurs when the denominator is zero. A zero denominator leaves the ratio undefined, so there's no value for inverted min-max normalisation to work with — not a relationship reversal, simply nothing to score. In practice, this only needs explicit handling in the program for P/FCF. This is because all the other valuation ratios are pre-calculated by a third party that returns 'Infinity' each time division by zero takes place. Since all infinite ratios are filtered out at the data retrieval stage, consideration of the zero-denominator case is otherwise unnecessary.

**Treatment of Edge Cases**

The treatment of any non-scorable value depends on which side of the ratio the invalidity falls on, not on how many underlying variables are affected. When invalid values occur on only one side of the ratio—that is, when all variables on the other side have positive, fixed values—each invalid value can be mapped to its closest scorable value. This treatment requires the other side of the ratio to contain only positive values because it provides an anchor against which the mapped values can be evaluated, making the resulting ratio a consistent, mathematically forced outcome.

Mapping invalid variables to their closest scorable values was chosen as the fairest way to represent them, given that leaving their values unchanged was not an option because, as established, inverted min-max normalisation cannot consistently score them.

Depending on whether the numerator or denominator variables are mapped to their closest scorable values, this treatment will result in either a maximum or a minimum score. For example: consider the P/E for a company with a negative E. Since P can be assumed positive, it provides the anchor value that permits the mapping treatment to be used. This means that the negative E can be treated as its closest scorable value, a very small positive E, making the P/E very high. If a company has a very high P/E, it would likely be scored very low by inverted min-max normalisation. Accordingly, companies with negative E are assigned the minimum score for their P/E.

It could be argued that this treatment is too lenient and that companies with a negative E should receive a point deduction. In the example above, the company with negative E is potentially an even weaker valuation opportunity than one with a very low positive E. The reason that the program chooses not to implement point deductions is because the P/E also depends on P. If penalisation were used, a company with a slightly negative E and very low P would lose points relative to a company with a very low positive E and very high P. However, based on an economic interpretation of the situation, the company with the negative E is likely the more attractive valuation opportunity.

The main exception to this treatment is when invalid variables span both sides of the ratio simultaneously. This requires both the numerator and denominator variables to be mapped to their closest scorable values, meaning neither side of the ratio remains fixed to act as an anchor for the other. This is problematic because a ratio is defined by the relative magnitude and sign of its numerator and denominator. When variables on both sides are mapped to their closest scorable values, the true value of both sides becomes obscured and information about this relative magnitude is lost, because nothing is known about how close the true values of the invalid variables are to their respective closest scorable values. For example, one variable's true negative value may lie much closer to its closest scorable value than another's, meaning that mapping both variables to those values does not preserve their true relationship. As a result, without an anchor, the mapped ratio can no longer be considered a mathematically forced outcome — the value it produces reflects the mapping itself, rather than any genuine relationship between the underlying variables.

Therefore, this case is instead treated by awarding a neutral 0.5 points. This was seen as a reasonable score to reflect a genuine absence of usable information about the company's valuation rather than any specific claim about it.

**Applying the Edge-Case Treatment**

Note: P/S can never take a non-scorable value, since both P and S are assumed positive, so 'score_for_ps()' is not discussed in the comments below.

In score_for_pe(), the following logic is applied when handling P/E values with a negative E:

If the P/E is negative, E must be negative because the numerator can be assumed to be positive. As discussed, when the denominator is negative and the numerator is positive, inverted min-max normalisation cannot be used for consistent scoring. Instead, since P provides an anchor value, the mapping treatment can be applied. This means that the negative E can be treated as its closest scorable value, a very small positive E, making the P/E very high. Therefore, when the P/E is negative, it's treated as a very high value and receives the minimum score.

In score_for_peg(), the following logic is applied when handling P/EG values with a negative E and/or negative G:

Since the numerator can be assumed to be positive, the following can be deduced: if P/EG is negative and P/E is positive then expected earnings growth is negative and earnings are positive. If P/EG is negative and P/E is negative then expected earnings growth is positive and earnings are negative. If P/EG is positive and P/E is negative then expected earnings growth and earnings are both negative. As discussed, when one or both denominator variables are negative, inverted min-max normalisation cannot be used for consistent scoring. Instead, since P provides an anchor value, the mapping treatment can be applied. This means that each negative denominator variable can be treated as its closest scorable value – a very small positive value. Independent of whether one or both of the denominator variables are negative, this treatment results in a very small positive denominator product and a very high P/EG value. Therefore, when the P/EG and/or the P/E is negative, the P/EG is treated as a very high value and receives the minimum score.

In score_for_ev_to_revenue(), the following logic is applied when handling EV/R values with a negative EV:

If the EV/R is negative, EV must be negative because R can be assumed to be positive. As discussed, when the numerator is negative and the denominator is positive, inverted min-max normalisation cannot be used for consistent scoring. Instead, since R provides an anchor value, the mapping treatment can be applied. This means that the negative EV can be treated as its closest scorable value – zero. Thus, when the EV/R is negative, it's treated as zero and assigned the maximum score.

In score_for_ev_to_ebitda(), the following logic is applied when handling EV/EBITDA values with a negative EV and/or negative EBITDA:

There are three scenarios for EV/EBITDA that require edge-case treatment: negative EV and positive EBITDA, positive EV and negative EBITDA, and negative EV and negative EBITDA. However, the first two of these three scenarios have already been encountered in the 'Applying the Edge-Case Treatment' section of this document. When EV is negative and EBITDA is positive, for the same reason as when scoring the EV/R, the EV/EBITDA is treated as zero and receives the maximum score. Likewise, when EV is positive and EBITDA is negative, for the same reason as when scoring the P/E, the EV/EBITDA is treated as a very high value and receives the minimum score. The last scenario, where the numerator and denominator variables are both negative, has not yet been encountered in the 'Applying the Edge-Case Treatment' section, so the breakdown of how it is handled needs a little bit more explanation. As discussed in the 'Why is Edge-Case Scoring Implemented?' section, when the numerator and denominator are both negative, inverted min-max normalisation cannot be used for consistent scoring. Additionally, since this case involves invalid variables spanning both sides of the ratio, based on the reasoning given in the 'Treatment of Edge Cases' section, it is not handled by mapping the numerator and denominator variables to their closest scorable values. Instead, it is treated by awarding a neutral score of 0.5 points.

In score_for_price_to_fcf(), the following logic is applied when handling P/FCF values with a non-positive FCF:

For the same reason as when scoring the P/E, each negative FCF is treated as a very low positive FCF, making the P/FCF a very high value. Therefore, when FCF is negative, the P/FCF is treated as a very high value and receives the minimum score.

However, since P/FCF is calculated in-house, the case where FCF equals zero must also be considered. As discussed, when the denominator is zero, inverted min-max normalisation cannot be used for scoring purposes simply because there is no defined value to score. Instead, since P provides an anchor value, the mapping treatment can be applied. This means that the invalid zero FCF can be treated as its closest scorable value, a very small positive FCF, making the P/FCF very high. Therefore, just like when FCF is negative, the P/FCF is treated as a very high value and receives the minimum score when FCF equals zero.

**Cases with One Metric Value for Normalisation**

Functions scoring metrics that can update totals without using inverted min-max normalisation have the potential to only pass the metric value for one company into 'assign_scores_to_stocks()'. When this occurs, the company's total is manually incremented by 0.5 points. This was chosen as a balanced score to allocate to the company given that the relative performance of its metric value cannot be assessed because there are no other values to compare it against.

**Adjusted Closing Price Clarification**

In display_results(), the code specifies 'Close' when retrieving prices for the user's chosen stock, but 'Closing Price (adj)' is used in the chart title. This is because newer versions of yfinance retrieve adjusted closing prices by default.

## **Addressing Potential Issues**

1. It is possible that issues with yfinance prevent stock information from being retrieved for any company. However, I have only encountered this issue once and it didn't last long. If it occurs, the program uses a try/except block to handle it without crashing.
2. The normalised scoring system is sensitive to outliers. However, keeping the cross-company comparison within the technology sector attempts to reduce both the number and extent of outlying data.
