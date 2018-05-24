/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [Region]
      ,[Country]
      ,[Period]
      ,[Advertiser]
      ,[Product_Category]
      ,[Category]
      ,[Subcategory]
      ,[Brand]
      ,[Subbrand]
      ,[Variant]
      ,[Network]
      ,[Creative]
      ,[Media]
      ,[Currency]
      ,[Spend]
      ,[TRP]
      ,[Normalized_Trp]
      ,[Insertions]
      ,[Impressions]
      ,[Spot_Length]
      ,[AcquireID]
  FROM [DM_1219_ColgateGlobal].[dbo].[DFID065658_SampleDataForDashboard_Extracted]

SELECT 
  [Region]
  ,[Country]
  ,[Advertiser]
  ,YEAR([Period]) AS Period
  ,SUM(CASE WHEN ISNUMERIC([Spend]) = 1
  THEN CAST([Spend] AS FLOAT)
  ELSE 0
  END) AS [Spend]
  ,COUNT(DISTINCT [Brand]) AS [BrandCount]
  FROM [DM_1219_ColgateGlobal].[dbo].[DFID065658_SampleDataForDashboard_Extracted]
  --WHERE YEAR([Period]) = '2017'
  GROUP BY
   [Region]
  ,[Country]
  ,[Advertiser]
  ,YEAR([Period])
  ORDER BY 
  1,2,3,4



    SELECT DISTINCT Brand
    FROM [DM_1219_ColgateGlobal].[dbo].[DFID065658_SampleDataForDashboard_Extracted]
	WHERE 
	Region = 'Latin America'
	AND
	Country = 'Argentina'
	AND
	Advertiser = 'COTY'
	AND 
	YEAR(Period) = '2018' -- => Koleston, Rimmel London, Sally Hansen
	--YEAR(Period) = '2017' -- => Coty, Koleston, Rimmel London, Sally Hansen

	


  SELECT 
  [Region]
  ,[Country]
  ,[Advertiser]
  ,YEAR([Period]) AS Period
  ,SUM(CASE WHEN ISNUMERIC([Spend]) = 1
  THEN CAST([Spend] AS FLOAT)
  ELSE 0
  END) AS [Spend]
  ,COUNT(DISTINCT [Brand]) AS [BrandCount]
  INTO [DM_1219_ColgateGlobal].[dbo].[DFID065658_Temp]
  FROM [DM_1219_ColgateGlobal].[dbo].[DFID065658_SampleDataForDashboard_Extracted]
  GROUP BY
   [Region]
  ,[Country]
  ,[Advertiser]
  ,YEAR([Period])
  ORDER BY 
  1,2,3,4 -- 1609 rows


  SELECT -- this gives me Country, Advertiser, Brand level spend; But I need a roll up for 
  [Region]
  ,[Country]
  ,[Advertiser]
  ,[Brand]
  ,YEAR([Period]) AS Period
  ,SUM(CASE WHEN ISNUMERIC([Spend]) = 1
  THEN CAST([Spend] AS FLOAT)
  ELSE 0
  END) AS [Spend]
  ,COUNT(DISTINCT [Brand]) AS [BrandCount]
  INTO [DM_1219_ColgateGlobal].[dbo].[DFID065658_Temp1]
  FROM [DM_1219_ColgateGlobal].[dbo].[DFID065658_SampleDataForDashboard_Extracted]
  GROUP BY
   [Region]
  ,[Country]
  ,[Advertiser]
  ,[Brand]
  ,YEAR([Period])
  ORDER BY 
  1,2,3,4 --9066 rows

  SELECT 
  a.[Region]
  ,a.[Country]
  ,a.[Advertiser]
  ,a.[Brand]
  ,a.[Period]
  ,a.[Spend] AS [SumByBrand]
  ,b.[Spend] AS [SumByAdvertiser]
  ,b.BrandCount AS [BrandCountByAdvertiser]
  FROM DFID065658_Temp1 as a
  LEFT JOIN DFID065658_Temp as b
  ON
	a.[Region] = b.[Region]
	AND a.[Country] = b.[Country]
	AND a.[Advertiser] = b.[Advertiser]
	--AND a.[Brand] = b.[Brand]
	AND a.[Period] = b.[Period]

	
WITH T1
AS (
	SELECT *
		,DENSE_RANK() OVER (
			PARTITION BY [Region]
			,[Country]
			,[Advertiser]
			,YEAR([Period]) ORDER BY Brand
			) AS [dr]
	FROM DFID065658_SampleDataForDashboard_Extracted
	)
	,T2
AS (
	SELECT *
		,MAX([dr]) OVER (
			PARTITION BY [Region]
			,[Country]
			,[Advertiser]
			,YEAR([Period])
			) AS UniqBrandCount
	FROM T1
	)
SELECT [Region]
	,[Country]
	,[Advertiser]
	,[Brand]
	,YEAR([Period]) AS [Period]
	,SUM(CASE 
			WHEN ISNUMERIC([Spend]) = 1
				THEN CAST([Spend] AS FLOAT)
			ELSE 0
			END) AS [Spend]
	,MAX(UniqBrandCount) AS UniqBrandCount
FROM T2
GROUP BY [Region]
	,[Country]
	,[Advertiser]
	,[Brand]
	,YEAR([Period])
ORDER BY [Region]
	,[Country]
	,[Advertiser]
	,YEAR([Period])
	,Brand

	
SELECT [Region]
	,[Country]
	,[Advertiser]
	,[Brand]
	,YEAR([Period]) AS [Period]
	,dense_rank() OVER (
		PARTITION BY [Region]
		,[Country]
		,[Advertiser]
		,YEAR([Period]) ORDER BY Brand
		) + dense_rank() OVER (
		PARTITION BY [Region]
		,[Country]
		,[Advertiser]
		,YEAR([Period]) ORDER BY Brand DESC
		) - 1 AS [BrandCount]
	,SUM(CASE 
			WHEN ISNUMERIC([Spend]) = 1
				THEN CAST([Spend] AS FLOAT)
			ELSE 0
			END) OVER (
		PARTITION BY [Region]
		,[Country]
		,[Advertiser]
		,[Brand]
		,YEAR([Period])
		) AS [Spend]
FROM [DM_1219_ColgateGlobal].[dbo].[DFID065658_SampleDataForDashboard_Extracted]
ORDER BY 1,2,3,4