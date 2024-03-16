from src.extensions.database import db
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func, cast, Interval, Text, text, alias, select, column
from sqlalchemy.orm import relationship
from src.models.event_names import EventName
from src.models.event_dimensions import EventDimension
from src.models.event_metrics import EventMetric
from src.models.dimensions import Dimension
from sqlalchemy.dialects.postgresql import INTERVAL
from src.models.allowed_event_dimensions import AllowedEventDimension
from sqlalchemy.dialects.postgresql import aggregate_order_by
from src.models.allowed_event_metrics import AllowedEventMetric
from src.models.metrics import Metric
from src.models.units import Unit
from sqlalchemy.orm import aliased
from sqlalchemy import JSON
from datetime import timedelta
import time
import json
import pandas as pd

colors = [
    (0, 153, 198),    # Cyan (#0099C6)
    (220, 57, 18),    # Red (#DC3912)
    (255, 153, 0),    # Orange (#FF9900)
    (16, 150, 24),    # Green (#109618)
    (170, 128, 255),   # Purple (#6633CC)
    (51, 102, 204),   # Blue (#3366CC)
    (221, 68, 119),   # Pink (#DD4477)
    (170, 170, 17),   # Olive (#AAAA11)
    (34, 170, 153),   # Turquoise (#22AA99)
    (153, 0, 153)    # Purple (#990099)
]

# Convert the colors to the required format
formatted_colors_table = ['#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in colors]
formatted_colors = ['rgba({}, {}, {}, 1)'.format(r, g, b) for r, g, b in colors]
formatted_bg_colors = ['rgba({}, {}, {}, 0.6)'.format(r, g, b) for r, g, b in colors]

def generate_datetime_range(start_datetime, end_datetime, granularity, timezone=0):
        if granularity == '2':
            freq = 'T'
        elif granularity == '3':
            freq = 'H'
        elif granularity == '4':
            freq = 'D'
        elif granularity == '5':
            freq = 'M'
        else:
            raise ValueError("Invalid granularity. Valid values are 'minute', 'hour', 'day', or 'month'.")

        index = pd.date_range(start=start_datetime, end=end_datetime, freq=freq)
        df = pd.DataFrame({"date": index})
        df["date"] = pd.to_datetime(df['date'], unit='s')
        df['date'] =  df['date'] + timedelta(hours=timezone)
        if granularity == '2':
            df['date'] = df['date'].dt.floor('T')
        elif granularity == '3':
            df['date'] = df['date'].dt.floor('H')
        elif granularity == '4':
            df['date'] = df['date'].dt.floor('D')
        elif granularity == '5':
            df['date'] = df['date'].dt.to_period('M').dt.to_timestamp()
        
        return df

class EventStat(db.Model):
    __tablename__ = 'event_stats'
    __table_args__ = {'schema': 'analytics'}

    event_id = Column(Integer, primary_key=True)
    lg_id = Column(Integer, ForeignKey('analytics.loggers.id'))
    en_id = Column(Integer, ForeignKey('analytics.event_names.id'))
    ev_ts = Column(TIMESTAMP(timezone=True), nullable=False)
    insertion_ts = Column(TIMESTAMP(timezone=True), server_default='now()', nullable=False)
    aw_id = Column(Integer, ForeignKey('analytics.agg_windows.id'))
    is_processed = Column(Integer, nullable=False, default=0)

    logger = relationship("Logger", lazy='joined')
    event_name = relationship("EventName", lazy="joined")
    agg_window = relationship("AggWindow", lazy="joined")


    @classmethod
    def stats(cls,
              logger,
              agg_window,
              timezone,
              datetime_from,
              datetime_to,
              event,
              dimension,
              metric,
              function,
              sort,
              form_data,
              n_rows=2,
              show_legend=True,
              show_cumsum=False):
        a = db.session.query(
            select([column("o_lg_id"), column("o_ev_ts"), column("o_event_name"), column("o_dims"), column("o_metrics")])
            .select_from(func.get_event_data(
                int(agg_window),
                int(event),
                int(logger),
                dimension,
                metric,
                function,
                datetime_from,
                datetime_to
                ).alias()).subquery()
        ).all()

        res = []
        for row in a:
            b = dict()
            b["ev_ts"] = row.o_ev_ts
            b["event_name"] = row.o_event_name
            for dim in row.o_dims:
                b["dim_"+str(dim.get("id"))] = dim.get("val")
            for metric in row.o_metrics:
                b["metric_"+str(metric.get("id"))+"["+str(metric.get("unit"))+"]"+"|||"+str(metric.get("function_id"))] = metric.get("val")

            res.append(b)
        
        df = pd.json_normalize(res)

        groupby_cols = [col for col in df.columns if col.startswith('dim_')]
        if(len(dimension) < 1):
                columns_to_drop = [col for col in df.columns if col.startswith('dim_')]
                df.drop(columns=columns_to_drop, inplace=True)
                df['dim_event_name'] = df['event_name'].copy()
                groupby_cols = ["dim_event_name"]

        aggregation_functions = {}
        if show_cumsum != True:
            aggregation_functions = {
                '1': 'sum',
                '2': 'min',
                '3': 'max'
            }

        try:
            agg_dict = {metric_id: aggregation_functions.get(f"{metric_id.split('|||')[-1]}", 'sum') for metric_id in df.columns if metric_id.startswith('metric_')}
            df['ev_ts'] = pd.to_datetime(df['ev_ts'], unit='s').dt.tz_localize(None)
            df['ev_ts'] =  df['ev_ts'] + timedelta(hours=timezone)
            
            res = df.groupby(groupby_cols).agg(agg_dict).reset_index()
            if(len(dimension) < 1):
                res.drop(columns=["dim_event_name"], inplace=True)


            for index in form_data.get("order", []):
                sort = True
                i = index.get("column", -1)
                if index.get("dir") == 'desc':
                    sort = False
                print("sort ", sort, index)
                res = res.sort_values(by=res.columns[i], ascending=sort)

            filter_val = form_data.get("search", {}).get("value", '')
            if filter_val != '':
                dim_columns = res.filter(regex='^dim_')

                matches = dim_columns.apply(lambda x: x.str.contains(filter_val, regex=True))

                rows_to_keep = matches.any(axis=1)
                res = res[rows_to_keep]
            
            dim_columns = res.filter(regex='^dim_')
            first_n_rows = dim_columns.iloc[:n_rows].values
            first_n_rows = ['|'.join(row) for row in first_n_rows]

            res.columns = res.columns.str.replace('dim_', '')
            res.columns = res.columns.str.replace('metric_', '')
            res = res.rename(columns=lambda x: x.split('|||')[0])
            # res = res.drop(columns=['event_name'])

            df = df.drop(columns=['event_name'])
            
            a = []
            i = 0
            # Loop through each combination of dimension values
            datetime_df = generate_datetime_range(datetime_from, datetime_to, agg_window, timezone)
            for group_name, group_df in df.groupby(groupby_cols):
                label = '|'.join(str(x) for x in group_name)
                if(len(dimension) == 1):
                    label = group_name
                elif(len(dimension) < 1):
                    label = group_name
                    first_n_rows = label
                    group_df = group_df.groupby("ev_ts").agg(agg_dict).reset_index()
                
                if((label not in first_n_rows)):
                    continue
                date_df = datetime_df
                merged_df = date_df.merge(group_df, left_on='date', right_on='ev_ts', how='left')
                merged_df.fillna(0, inplace=True)
                
                if show_cumsum == True:
                    first_metric_column = next((col for col in df.columns if col.startswith('metric_')), None)
                    merged_df[first_metric_column] = merged_df[first_metric_column].cumsum()
                
                # merged_df = merged_df.loc[:, ['date'] + [col for col in df.columns if 'metric_' in col]]
                metric_col = merged_df.filter(like='metric_').squeeze()  # Assuming only one 'metric_' column exists


                # Convert 'metric_' column to a Python list
                metric_list = metric_col.tolist()
                
                b = dict()
                b["data"] = metric_list #(merged_df.to_json(orient='records'))
                b["label"] = label
                for index, item in enumerate(first_n_rows):
                    if len(dimension) < 1:
                        b["borderColor"] = formatted_colors[0]
                        b["backgroundColor"] = formatted_bg_colors[0]
                        
                    if item==label:
                        b["borderColor"] = formatted_colors[index]
                        b["backgroundColor"] = formatted_bg_colors[index]
                        break
                # b["fill"] = "false"
                b["showLine"] = "true"
                if show_cumsum == True:
                    b["stepped"] = True
                a.append(b)
                i += 1

        except Exception as e:
            print(e)
            return {
            "table": {"data": '[]', "header": []},
            "chart": {"settings": {"show_legend": show_legend}, "datasets": [], "labels": []},
            "last_update": 1,
            "error": f"{e}"
            }

        return {
            "table": {"data": res.to_json(orient='records'), "colors": formatted_colors_table[:n_rows], "header": []},
            "chart": {"settings": {"show_legend": show_legend}, "datasets": a, "labels": datetime_df['date'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()},
            "last_update": 1
            }
