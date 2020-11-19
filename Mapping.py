
import openpyxl
import openpyxl.utils
from us_state_abbrev import us_state_abbrev
import plotly.graph_objects

def get_excel_rows(file_name):
    excel_file = openpyxl.load_workbook(file_name)
    first_sheet = excel_file.active
    all_data = first_sheet.rows
    return all_data


def main():
    income_data = get_excel_rows("MedianIncomeInflationAdjusted.xlsx")
    state_abbreviation_list = []
    income_changes = []
    for income_row in income_data:
        state_name = income_row[0].value
        if not state_name in us_state_abbrev:
            continue
        income2018 = income_row[1].value
        old_income_col = openpyxl.utils.column_index_from_string("Z")-1
        income2008 = income_row[old_income_col].value
        change_in_income = income2018 - income2008
        state_abbrev = us_state_abbrev[state_name]
        state_abbreviation_list.append(state_abbrev)
        income_changes.append(change_in_income)

    income_change_map = plotly.graph_objects.Figure(
        data=plotly.graph_objects.Choropleth(
            locations= state_abbreviation_list,
            z = income_changes,
            locationmode = "USA-states",
            colorscale = "RdBu",
            colorbar_title = "Income Changes since 2008"
    ))
    income_change_map.update_layout(title_text="Inflation Adjusted Real income change since 2008", geo_scope="usa",)
    income_change_map.show()



main()