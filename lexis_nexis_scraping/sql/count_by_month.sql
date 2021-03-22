select COUNT(id),
    MONTH(date),
    YEAR(date)
from articles
GROUP BY MONTH(date),
    YEAR(date);
