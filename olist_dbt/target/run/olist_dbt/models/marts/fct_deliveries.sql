
  
    

  create  table "olist_db"."public"."fct_deliveries__dbt_tmp"
  
  
    as
  
  (
    with orders as (
    select * from "olist_db"."public"."stg_orders"
),
items as (
    select * from "olist_db"."public"."stg_order_items"
),
customers as (
    select * from "olist_db"."public"."olist_customers_dataset"
),
sellers as (
    select * from "olist_db"."public"."olist_sellers_dataset"
)

select
    o.order_id,
    o.customer_id,
    i.seller_id,
    c.customer_state,
    s.seller_state,
    i.freight_value,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    
    extract(epoch from (o.order_delivered_customer_date - o.order_purchase_timestamp)) / (24 * 3600) as delivery_time_days,
    
    extract(epoch from (o.order_delivered_customer_date - o.order_estimated_delivery_date)) / (24 * 3600) as estimated_error_days,
    
    case 
        when extract(epoch from (o.order_delivered_customer_date - o.order_estimated_delivery_date)) > 0 then 1 
        else 0 
    end as is_late

from orders o
join items i on o.order_id = i.order_id
join customers c on o.customer_id = c.customer_id
join sellers s on i.seller_id = s.seller_id
where o.order_status = 'delivered'
  and o.order_delivered_customer_date is not null
  );
  