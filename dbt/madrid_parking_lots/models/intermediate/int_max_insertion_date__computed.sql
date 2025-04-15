with
max_insertion_date as (

  select
    max(insertion_date) as max_insertion_date
  from
        {{ ref('stg_calles_zona_ser__madrid_parking_lots') }}

),

zona_ser_max_insertion_date as (

    select 
        gis_x,
        gis_y,
        distrito,
        calle,
        numero_finca,
        color,
        bateria_linea,
        numero_plazas
    from 
        calles_zona_ser_raw_prueba raw 
            inner join 
                max_insertion_date max_date on
                    raw.insertion_date = max_date.max_insertion_date

)

select * from zona_ser_max_insertion_date
