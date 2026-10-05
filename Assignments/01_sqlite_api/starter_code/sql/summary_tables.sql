-- Pre-aggregated rollup used by the /fast versions of Q13 and Q14.
-- It is a snapshot: rows inserted later (Phase 4) do NOT show up here until
-- you rebuild it. Real systems refresh it on a schedule or with triggers.
DROP TABLE IF EXISTS monthly_sales;
CREATE TABLE monthly_sales (
    month         TEXT NOT NULL,      -- 'YYYY-MM'
    state_code    TEXT NOT NULL,
    department    TEXT NOT NULL,
    num_purchases INTEGER NOT NULL,
    revenue       NUMERIC NOT NULL,
    PRIMARY KEY (month, state_code, department)
);
INSERT INTO monthly_sales
SELECT substr(pu.purchase_date, 1, 7), z.state_code, pu.department,
       COUNT(*), SUM(pu.amount)
FROM purchases pu
JOIN customers c ON c.customer_id = pu.customer_id
JOIN zipcodes  z ON z.zipcode     = c.zipcode
GROUP BY 1, 2, 3;
