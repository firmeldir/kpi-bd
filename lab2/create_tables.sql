CREATE TABLE IF NOT EXISTS contragents
(
    IPN          int PRIMARY KEY,
    name         varchar(255) NOT NULL,
    phone_number char(15) NOT NULL
);

CREATE TABLE IF NOT EXISTS warehouses
(
    warehouse_id          serial PRIMARY KEY,
    city      text NOT NULL,
    office_number char(15) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders
(
    order_id               serial PRIMARY KEY,
    recipients_date    date NOT NULL,
    order_date    date NOT NULL,
    shipping_cost     money NOT NULL,
    sender_ipn        int NOT NULL,
    recipient_ipn     int NOT NULL,
    warehouse_id serial NOT NULL,
    CONSTRAINT recipient_ipn FOREIGN KEY (recipient_ipn)
        REFERENCES contragents (IPN)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    CONSTRAINT sender_ipn FOREIGN KEY (sender_ipn)
        REFERENCES contragents (IPN)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    CONSTRAINT fk_warehouse_orders FOREIGN KEY (warehouse_id)
        REFERENCES public.warehouses (warehouse_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS goods
(
    good_id          serial PRIMARY KEY,
    height      int NOT NULL,
    width       int NOT NULL,
    depth       int NOT NULL,
    weight      int NOT NULL,
    description text,
    order_id serial NOT NULL,
    CONSTRAINT fk_order_goods FOREIGN KEY (order_id)
        REFERENCES public.orders (order_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
CREATE INDEX IF NOT EXISTS goods_descriptions ON goods USING gin(to_tsvector('english', description));
