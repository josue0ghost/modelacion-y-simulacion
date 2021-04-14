
SELECT
	teamID
	,SUM(Singles) Singles
	,SUM(Doubles) Doubles
	,SUM(Triples) Triples
	,SUM(HomeRuns) HomeRuns
	,SUM(BaseOnBalls) BaseOnBalls
	,SUM(HitByPitch) HitByPitch
	,SUM(Sacrifice) Sacrifice
	,SUM(DoublePlayed) DoublePlayed
	,SUM(StrikeOut) StrikeOut
	,SUM(FGOuts) FGOuts
	,SUM(Plates) Plates
FROM
(SELECT [playerID]
	  ,[teamID]
	  ,[H]-[2B]-[3B]-[HR] AS [Singles]
	  ,[2B] AS [Doubles]
	  ,[3B] AS [Triples]
	  ,[HR] AS [HomeRuns]
	  ,[BB] AS [BaseOnBalls]
	  ,CAST([HBP] AS float) AS [HitByPitch]
	  ,CAST([SF] AS float) AS [Sacrifice]
	  ,[GIDP] AS [DoublePlayed]
	  ,[SO] AS [StrikeOut]
	  ,[AB]-[H]-[SO]-[GIDP] AS [FGOuts]
	  ,[AB]+[BB]+CAST([HBP] AS float)+CAST([SF] AS float) AS [Plates]
FROM [modelacion].[dbo].[Batting]
WHERE [yearID] = 2020) filtrado
GROUP BY teamID

