import streamlit as st
import requests
from datetime import datetime

API_key = 'b23114a6e1225d45ba214abf4daec1d9'

st.image("cloud.jpg", use_column_width=True)

st.title("Diamo un'occhiata al tempo")
# Input testo dall'utente
city_name = st.text_input('Scrivi il nome della città')

# Define weather keys and their descriptions
weather_keys = {
    'temp': '**La temperatura** è di **{}**°C',
    'temp_min': '**La temperatura minima** è di **{}**°C',
    'temp_max': '**La temperatura massima** è di **{}**°C',
    'pressure': '**La pressione** è **{}** hPa',
    'humidity': '**L\'umidità** è del **{}**%',
    'wind_speed': '**La velocità del vento** è **{}** m/s'
}

def kelvin_to_celsius(kelvin):
    return round(kelvin - 273.15, 1)

if st.button('controlliamo'):
    if city_name:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}'
        result = requests.get(url)
        if result.status_code == 200:
            json = result.json()
            main = json.get('main', {})
            wind = json.get('wind', {})

            data = {
                'temp': kelvin_to_celsius(main.get('temp')),
                'temp_min': kelvin_to_celsius(main.get('temp_min')),
                'temp_max': kelvin_to_celsius(main.get('temp_max')),
                'pressure': main.get('pressure'),
                'humidity': main.get('humidity'),
                'wind_speed': wind.get('speed')
            }

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Previsioni di oggi")
                for key, message in weather_keys.items():
                    value = data.get(key)
                    if value is not None:
                        st.write(message.format(value))
                        st.divider()
            
            # Fetching forecast data
            url2 = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_key}'
            forecast_result = requests.get(url2)
            if forecast_result.status_code == 200:
                forecast_json = forecast_result.json()
                forecast_list = forecast_json.get('list', [])
                forecast_city = forecast_json.get('city', {})
                sunset_timestamp = forecast_city.get('sunset', 0)
                sunset_time = datetime.fromtimestamp(sunset_timestamp).strftime('%H:%M:%S')

                with col2:
                    st.subheader(f"**Previsioni per oggi fino alle 00:00**")
                    for entry in forecast_list:
                        forecast_time = datetime.fromtimestamp(entry['dt'])
                        if forecast_time.date() == datetime.now().date() and forecast_time.hour <= 23:
                            feels_like = kelvin_to_celsius(entry['main']['feels_like'])
                            wind_speed = entry['wind']['speed']
                            precipitation = entry['rain'].get('3h', 0) if 'rain' in entry else 0
                            st.write(f"Ora: {forecast_time.strftime('%H:%M')}")
                            st.write(f"**Temperatura percepita:** {feels_like}°C")
                            st.write(f"**Velocità del vento:** {wind_speed} m/s")
                            st.write(f"**Precipitazioni:** {precipitation} mm")
                            st.divider()
                    st.write(f"**Orario del tramonto:** {sunset_time}")
            else:
                st.write("Previsioni non disponibili.")
        else:
            st.write("Città non trovata. Per favore, prova con un'altra città.")
