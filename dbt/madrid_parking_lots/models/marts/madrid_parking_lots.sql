{{
  config(
        materialized='table',
        bind=False
    )
}}
with
madrid_parking_lots as (

    select
        longitude as longitud,
        latitude as latitud,
        barrio,
        calle,
        numero_finca as num_finca,
        regexp_replace(color, '^\d+\s*', '') as color,
        bateria_linea,
        numero_plazas as num_plazas
    from
        {{ ref('int_coordinates__computed') }}

)

select * from madrid_parking_lots
