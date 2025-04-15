with
coordinates_computed as (

    select
        gis_x,
        gis_y,
        ST_X(ST_Transform(ST_SetSRID(ST_MakePoint(gis_x, gis_y), 25830), 4326)) AS longitude,
        ST_Y(ST_Transform(ST_SetSRID(ST_MakePoint(gis_x, gis_y), 25830), 4326)) AS latitude,
        distrito,
        calle,
        numero_finca,
        color,
        bateria_linea,
        numero_plazas
    from 
        {{ ref('int_max_insertion_date__computed') }}

)

select * from coordinates_computed
