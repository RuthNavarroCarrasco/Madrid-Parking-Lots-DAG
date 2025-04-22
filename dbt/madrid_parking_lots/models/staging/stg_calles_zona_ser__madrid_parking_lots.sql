with
source as (

    select 
        insertion_date,
        gis_x,
        gis_y,
        distrito as barrio,
        calle,
        numero_finca,
        color,
        bateria_linea,
        numero_plazas
    from
        {{ source('public', 'calles_zona_ser_raw_prueba') }}
)

select * from source
