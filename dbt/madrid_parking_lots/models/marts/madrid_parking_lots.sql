{{
  config(
        materialized='table',
        bind=False
    )
}}
with
madrid_parking_lots as (

    select
        longitude,
        latitude,
        distrito as district,
        calle as street,
        numero_finca,
        color,
        bateria_linea as parking_type,
        numero_plazas as total_parking_lots
    from
        {{ ref('int_coordinates__computed') }}

)

select * from madrid_parking_lots
