
  create view "olist_db"."public"."stg_orders__dbt_tmp"
    
    
  as (
    select
    order_id,
    customer_id,
    order_status,
    cast(order_purchase_timestamp as timestamp) as order_purchase_timestamp,
    cast(order_delivered_customer_date as timestamp) as order_delivered_customer_date,
    cast(order_estimated_delivery_date as timestamp) as order_estimated_delivery_date
from "olist_db"."public"."olist_orders_dataset"
  );