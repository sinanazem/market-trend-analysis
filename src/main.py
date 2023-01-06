import pandas as pd
# from crawlers.blackrock import BlackRockInsights
from crawlers.vanguard import VanguardInsights
from utils import DataBaseClass

# BlackRock
# obj = BlackRockInsights('https://www.blackrock.com/us/individual/insights')
# blackrock_insight_list = obj.get_article_insight()
# blackrock_df = pd.DataFrame(blackrock_insight_list)


# Vanguard
vanguard_insight_obj = VanguardInsights('https://advisors.vanguard.com/insights/all')
vanguard_insight_list = vanguard_insight_obj.get_article_insight()
vanguard_df = pd.DataFrame(vanguard_insight_list)

# Store data

obj_data_base_class = DataBaseClass('postgres', 'sina2000', '0.0.0.0', 5432, 'insights_db')
obj_data_base_class.store_data(vanguard_df, sql_table_name='insights_data')