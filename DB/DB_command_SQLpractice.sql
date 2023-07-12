
---------------- SQL 실습 문제 풀이 시작-------------------
-- data: https://www.w3schools.com/sql/trysql.asp?filename=trysql_asc
-- Q. Tokyo에 위치한 공급자(Supplier)가 생산한 상품(Products) 목록 조회
-- Table: Suppliers, Products
SELECT Products.*, Supplier.SupplierID
FROM Products
    INNER JOIN Suppliers
    ON Products.SupplierID = Suppliers.SupplierID
WHERE Suppliers.City = 'Tokyo';


-- Q. 분류(CategoryName)가 Seafood인 상품명(ProductName) 조회
-- Table: Categories, Products
SELECT ProductName, CategoryName
FROM Products
    LEFT JOIN Categories
    ON Categories.CategoryID = Products.CategoryID
WHERE CategoryName = 'Seafood';


-- Q. 공급자(Supplier)가 공급한 상품의 공급자 국가(Country), 
-- 카테고리별로 상품건수와 평균가격 조회
-- Table: Suppliers, Products, Categories
-- 방법 1 >
SELECT S.Country, C.CategoryName, 
    COUNT(*) AS NumProduct, AVG(P.Price) AS AvgPrice
FROM Products AS P
    INNER JOIN Suppliers AS S
    ON P.SupplierID = S.SupplierID
    INNER JOIN Categories AS C
    ON P.CategoryID = C.CategoryID
GROUP BY S.Country, C.CategoryID;


-- 방법 2 >
SELECT S.Country, C.CategoryName, 
    COUNT(*) AS NumProduct, AVG(P.Price) AS AvgPrice
FROM Products AS P, Suppliers AS S,Categories AS C
WHERE P.SupplierID = S.SupplierID and P.CategoryID = C.CategoryID
GROUP BY S.Country, C.CategoryID;


-- Q. 주문별 주문자명(CustomerName), 직원명(LastName), 배송자명(ShipperName), 주문상세갯수
-- Table: Orders, OrderDetails, Customers, Employees, Shippers
-- 방법 1 >
SELECT O.OrderID, C.CustomerName, E.LastName, S.ShipperName, 
    COUNT(OD.OrderDetailID) AS SUM
FROM Orders AS O
    INNER JOIN Customers AS C
    ON O.CustomerID = C.CustomerID
    INNER JOIN employees AS E
    ON O.EmployeeID = E.EmployeeID
    INNER JOIN Shippers AS S
    ON O.ShipperID = S.ShipperID
    INNER JOIN OrderDetails AS OD
    ON O.OrderID = OD.OrderID
GROUP BY O.OrderID;

-- 방법 2 > SubQuery를 Table로 활용 (서브쿼리를 활용한 방법 2보다 방법 1의 속도가 더 빠름)
SELECT OD.OrderDetailID, OI.OrderID, 
    OI.CustomerName, OI.LastName, OI.ShipperName
FROM OrderDetails AS OD
LEFT JOIN (
    SELECT O.OrderID, C.CustomerName, E.LastName, S.ShipperName
    FROM Orders AS O
    INNER JOIN Customers AS C
    ON O.CustomerID=C.CustomerID
    INNER JOIN Employees AS E
    ON O.EmployeeID=E.EmployeeID
    INNER JOIN Shippers AS S
    ON O.ShipperID=S.ShipperID
) AS OI -- OrderInfo
ON OD.OrderID=OI.OrderID;


-- Q. 판매량(Quantity) 상위 TOP 3 공급자(supplier) 목록 조회
-- Table: Suppliers, Products, OrderDetails
SELECT S.*, SUM(OD.Quantity) AS SumQuantity
FROM Products AS P 
    INNER JOIN Suppliers AS S
    ON P.SupplierID = S.SupplierID
    INNER JOIN OrderDetails AS OD
    ON P.ProductID = OD.ProductID
GROUP BY S.SupplierID
ORDER BY SumQuantity DESC
LIMIT 3;


-- Q. 상품분류(Category)별, 고객지역별(City) 판매량 많은 순 정렬
-- Table: Order, OrderDetails, Customers, Categories, Products
SELECT CA.CategoryName, CU.City, SUM(OD.Quantity) AS SumQuantity
FROM Categories AS CA
    INNER JOIN Products AS P
    ON CA.CategoryID = P.CategoryID
    INNER JOIN OrderDetails AS OD
    ON P.ProductID = OD.ProductID
    INNER JOIN Orders AS O
    ON OD.OrderID = O.OrderID
    INNER JOIN Customers AS CU
    ON O.CustomerID = CU.CustomerID
GROUP BY CA.CategoryName, CU.City
ORDER BY SumQuantity DESC;


-- Q. 고객국가(Country)가 USA이고, 상품별 판매량(Quantity)의 합이 많은순으로 정렬
-- Table: Customers, Products, Orders, OrderDetails
SELECT P.ProductName, CU.Country, SUM(OD.Quantity) AS SumQuantity
FROM OrderDetails AS OD
    INNER JOIN Products AS P
    ON OD.ProductID = P.ProductID
    INNER JOIN Orders AS O
    ON OD.OrderID = O.OrderID
    INNER JOIN Customers AS CU
    ON O.CustomerID = CU.CustomerID
WHERE CU.Country = 'USA'
GROUP BY P.ProductName
ORDER BY SumQuantity DESC


-- Q. Tokyo에 위치한 공급자(Supplier)가 생산한 상품 목록에 대한 VIEW 생성
-- Table: Suppliers, Products
CREATE VIEW Tokyo_Product(
    ProductID, ProductName, SupplierName, Unit, Price)
AS
SELECT ProductID, ProductName, SupplierName, Unit, Price
FROM Products AS P
    INNER JOIN Suppliers AS S
    ON P.SupplierID = S.SupplierID
WHERE S.City = 'Tokyo';

-- VIEW 삭제
DROP VIEW Tokyo_Product;


-- Q. 분류(CategoryName)가 Seafood인 상품명(ProductName)에 대한 VIEW 생성
-- Table: Categories, Products
CREATE VIEW Seafood_Product(ProductName)
AS 
SELECT P.ProductName
FROM Products AS P
    INNER JOIN Categories AS C
    ON P.CategoryID = C.CategoryID
WHERE C.CategoryName = 'Seafood';


---------------- SQL 실습 문제 풀이 끝-------------------


------------------- ERD 실습 시작 -----------------------
-- https://www.erdcloud.com/myPage 
-- data: https://www.w3schools.com/sql/trysql.asp?filename=trysql_asc
-- 결과물 https://www.erdcloud.com/d/ZH38cLGQHajJiRPdz
--------------------------------------------------

-- 1. Student 테이블 생성
CREATE TABLE Students(
    StudentID INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(32),
    Age INT,
    Address VARCHAR(255),
    PRIMARY KEY(StudentID)
);

-- 2. Grades 테이블 생성
CREATE TABLE Grades(
    GradeID INT NOT NULL AUTO_INCREMENT,
    StudentID INT,
    Math INT,
    English INT,
    Science INT,
    PRIMARY KEY(GradeID)
);

-- 3. Value 입력하기
INSERT INTO Students(Name, Age, Address) 
    VALUES('홍길동', 30, '인천');
INSERT INTO Students(Name, Age, Address)
    VALUES('이연걸', 60, '서울');
INSERT INTO Students(Name, Age, Address)
    VALUES('이몽룡', 42, '대전');
INSERT INTO Students(Name, Age, Address) 
    VALUES('성춘향', 27, '경기');

INSERT INTO Grades(StudentID, Math, English, Science) 
    VALUES(1, 90, 80, 50);
INSERT INTO Grades(StudentID, Math, English, Science)
    VALUES(2, 69, 76, 65);
INSERT INTO Grades(StudentID, Math, English, Science)
    VALUES(3, 98, 87, 97);
INSERT INTO Grades(StudentID, Math, English, Science)
    VALUES(4, 87, 67, 79);


-- 3-1. 테이블 업데이트 및 삭제 연습
UPDATE Students SET Age = 50 WHERE StudentID = 1;
UPDATE Students SET Address = '광주' WHERE StudentID = 2;
DELETE FROM Students WHERE Age = 42;



-- 4. Foreign key로 테이블 연결
ALTER TABLE Grades ADD CONSTRAINT fk_grade_student FOREIGN KEY(StudentID)
        REFERENCES Students(StudentID);

ALTER TABLE Grades MODIFY COLUMN StudentID INT NOT NULL;

---------------------- ERD 실습 끝 -----------------------


--------------------- INDEX 실습 시작 -------------------
-- 테이블 생성
CREATE TABLE Users(
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(32) UNIQUE,
    password VARCHAR(64),
    PRIMARY KEY(id)
);


-- INDEX 생성
CREATE INDEX idx_username ON Users(username);

-- INDEX 확인
SHOW INDEX FROM Users;

-- INDEX 삭제
DROP INDEX idx_username ON Users;

-- INDEX 중복 추가 에러 확인
INSERT INTO Users(username, password) VALUES('user1', '1234');
--ERROR 1062 (23000): Duplicate entry 'user1' for key 'username'

--------------------- INDEX 실습 끝 -------------------