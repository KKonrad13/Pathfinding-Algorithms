# Implementation of pathfinding algorithms 

## Data

Data colected from [Open Data Wrocław](https://opendata.cui.wroclaw.pl/dataset/rozkladjazdytransportupublicznegoplik_data).

### Data representation

| Company      | Line          | Departure Time | Arrival Time | Start Stop           | End Stop             | Start Stop Lat | Start Stop Lon | End Stop Lat | End Stop Lon |
|--------------|---------------|----------------|--------------|----------------------|----------------------|----------------|----------------|--------------|--------------|
| MPK Autobusy | A             | 20:52:00       | 20:53:00     | Zajezdnia Obornicka  | Paprotna             | 51.14873744    | 17.02106859    | 51.14775215  | 17.02053929  |
| MPK Autobusy | A             | 20:53:00       | 20:54:00     | Paprotna             | Obornicka (Wołowska) | 51.14775215    | 17.02053929    | 51.144385    | 17.023735    |
| MPK Autobusy | A             | 20:54:00       | 20:55:00     | Obornicka (Wołowska) | Bezpieczna           | 51.144385      | 17.023735      | 51.14136001  | 17.02637623  |
| ...          | ...           | ...            | ...          | ...                  | ...                  | ...            | ...            | ...          | ...          |           
