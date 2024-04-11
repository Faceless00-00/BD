-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 11 2024 г., 03:45
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `AdvertisingCompany`
--

DELIMITER $$
--
-- Процедуры
--
CREATE DEFINER=`root`@`%` PROCEDURE `AddEarning` (`earning_date_time` DATETIME, `earning_amount` INT, `earning_operation_type_id` INT, `earning_agent_id` INT)   BEGIN 
    INSERT INTO Earnings (date_time, amount, operation_type_id, agent_id) 
    VALUES (earning_date_time, earning_amount, earning_operation_type_id, earning_agent_id); 
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `get_out_list` (IN `name` VARCHAR(100))   BEGIN
SELECT id, salary FROM Agents WHERE full_name = name;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Структура таблицы `Agents`
--

CREATE TABLE `Agents` (
  `id` int NOT NULL,
  `full_name` varchar(50) DEFAULT NULL,
  `salary` int DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `privilege` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Agents`
--

INSERT INTO `Agents` (`id`, `full_name`, `salary`, `email`, `privilege`) VALUES
(1, 'John Doe', 5000, 'john@example.com', 1),
(2, 'Jane Smith', 6000, 'jane@example.com', 0),
(3, 'Daniil Suvorov', 10000, 'dan@mail.ru', 0);

-- --------------------------------------------------------

--
-- Структура таблицы `Children`
--

CREATE TABLE `Children` (
  `id` int NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `privilege` int DEFAULT NULL,
  `agent_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Children`
--

INSERT INTO `Children` (`id`, `name`, `date_of_birth`, `privilege`, `agent_id`) VALUES
(1, 'Alice Doe', '2010-05-15', 0, 1),
(2, 'Bob Smith', '2015-08-20', 1, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `Deductions`
--

CREATE TABLE `Deductions` (
  `id` int NOT NULL,
  `earning_id` int DEFAULT NULL,
  `deduction_type_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Deductions`
--

INSERT INTO `Deductions` (`id`, `earning_id`, `deduction_type_id`) VALUES
(1, 1, 1),
(2, 2, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `DeductionTypes`
--

CREATE TABLE `DeductionTypes` (
  `id` int NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `amount` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `DeductionTypes`
--

INSERT INTO `DeductionTypes` (`id`, `name`, `amount`) VALUES
(1, 'Agent Privilege 5%', 5),
(2, 'Child Deduction 7%', 7),
(3, 'Child Deduction with Privilege 12%', 12);

-- --------------------------------------------------------

--
-- Структура таблицы `Earnings`
--

CREATE TABLE `Earnings` (
  `id` int NOT NULL,
  `date_time` datetime DEFAULT NULL,
  `amount` int DEFAULT NULL,
  `operation_type_id` int DEFAULT NULL,
  `agent_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Earnings`
--

INSERT INTO `Earnings` (`id`, `date_time`, `amount`, `operation_type_id`, `agent_id`) VALUES
(1, '2024-03-28 08:00:00', 5000, 1, 1),
(2, '2024-03-28 08:00:00', 6000, 1, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `OperationTypes`
--

CREATE TABLE `OperationTypes` (
  `id` int NOT NULL,
  `name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `OperationTypes`
--

INSERT INTO `OperationTypes` (`id`, `name`) VALUES
(1, 'Payroll'),
(2, 'Tax');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Agents`
--
ALTER TABLE `Agents`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `Children`
--
ALTER TABLE `Children`
  ADD PRIMARY KEY (`id`),
  ADD KEY `agent_id` (`agent_id`);

--
-- Индексы таблицы `Deductions`
--
ALTER TABLE `Deductions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `earning_id` (`earning_id`),
  ADD KEY `deduction_type_id` (`deduction_type_id`);

--
-- Индексы таблицы `DeductionTypes`
--
ALTER TABLE `DeductionTypes`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `Earnings`
--
ALTER TABLE `Earnings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `operation_type_id` (`operation_type_id`),
  ADD KEY `agent_id` (`agent_id`);

--
-- Индексы таблицы `OperationTypes`
--
ALTER TABLE `OperationTypes`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Agents`
--
ALTER TABLE `Agents`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `Children`
--
ALTER TABLE `Children`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `Deductions`
--
ALTER TABLE `Deductions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `Earnings`
--
ALTER TABLE `Earnings`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `Children`
--
ALTER TABLE `Children`
  ADD CONSTRAINT `children_ibfk_1` FOREIGN KEY (`agent_id`) REFERENCES `Agents` (`id`);

--
-- Ограничения внешнего ключа таблицы `Deductions`
--
ALTER TABLE `Deductions`
  ADD CONSTRAINT `deductions_ibfk_1` FOREIGN KEY (`earning_id`) REFERENCES `Earnings` (`id`),
  ADD CONSTRAINT `deductions_ibfk_2` FOREIGN KEY (`deduction_type_id`) REFERENCES `DeductionTypes` (`id`);

--
-- Ограничения внешнего ключа таблицы `Earnings`
--
ALTER TABLE `Earnings`
  ADD CONSTRAINT `earnings_ibfk_1` FOREIGN KEY (`operation_type_id`) REFERENCES `OperationTypes` (`id`),
  ADD CONSTRAINT `earnings_ibfk_2` FOREIGN KEY (`agent_id`) REFERENCES `Agents` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
