# 🚀 Astro Project: Madrid Parking Lots ELT

This project extracts, loads, and transforms data about parking lots in Madrid using Airflow and the [Datos Abiertos del Ayuntamiento de Madrid](https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=4973b0dd4a872510VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default) API.

---

## 🛠 First Steps

1. **Install Astro CLI**
   ```bash
   curl -sSL https://install.astronomer.io | sudo bash
   ```

2. **Login to Astro**
   ```bash
   astro login
   ```

3. **Deploy your DAG**
   ```bash
   astro deploy
   ```
   🎉 Once deployed, view your DAG in Astro and open it in Airflow.

---

## 🧪 Local Development

Start your Airflow environment:
```bash
astro dev start
```

Stop it when you're done:
```bash
astro dev stop
```

---

## 📁 Project Structure

- `dags/`
  - `madrid_parking_lots.py`: ELT pipeline for Madrid parking lot data using a public API.

---
