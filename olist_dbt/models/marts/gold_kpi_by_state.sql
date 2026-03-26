with fct as (
    select * from {{ ref('fct_deliveries') }}
)

select
    customer_state,
    count(distinct order_id) as total_orders,
    sum(is_late) as late_orders,
    avg(delivery_time_days) as avg_delivery_time,
    avg(freight_value) as avg_freight_value,
    
    case 
        when count(distinct order_id) > 0 then 
            ((count(distinct order_id) - sum(is_late))::numeric / count(distinct order_id)) * 100 
        else 0 
    end as ontime_delivery_rate

from fct
group by customer_state
