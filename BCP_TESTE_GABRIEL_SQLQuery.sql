
-- Lista de Debêntures
SELECT COUNT(BCP_Codigo) AS Quantidade_BCP_Debentures_Dia_Anterior
FROM BCP_Dados
WHERE BCP_Data = CAST(DATEADD(DAY, -1, GETDATE()) AS DATE);

-- Durantion Média
SELECT AVG(BCP_Duration) AS Media_BCP_Duration
FROM BCP_Dados
WHERE BCP_Data IN (
    SELECT BCP_Data
    FROM BCP_Dados
    WHERE DATENAME(WEEKDAY, BCP_Data) NOT IN ('Saturday', 'Sunday')
    ORDER BY BCP_Data DESC
    OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY
)


-- Códigos únicos VALE S/A
SELECT DISTINCT BCP_Codigo
FROM BCP_Dados
WHERE BCP_Nome = 'VALE S/A';