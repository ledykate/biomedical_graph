drop database if exists biomedical_indicators;
CREATE SCHEMA IF NOT EXISTS biomedical_indicators DEFAULT CHARACTER SET utf8;
USE biomedical_indicators; # подключение

# Литературный источник (для доп.имени показателя)
CREATE TABLE Literatures(
	idLiteratures INT AUTO_INCREMENT NOT NULL PRIMARY KEY, # ID источника
	Lit_website TEXT(10000), # Сайт источника
	Lit_title TEXT(10000) # Библиографическое описание
);

# Источник порядка проведения методики
CREATE TABLE Source_method(
	idSource_method INT AUTO_INCREMENT NOT NULL PRIMARY KEY, # ID источника методики
	Source_website TEXT(10000), # Сайт источника
	Source_title TEXT(10000) # Библиографическое описание
);

# Тип показателя: первичный или вторичный
CREATE TABLE Type_indicator(
	idType_indicator INT AUTO_INCREMENT NOT NULL PRIMARY KEY, # ID типа показателя
	Name_type_indicator VARCHAR(50) NOT NULL # Название типа: первичный или вторичный
);

# Язык, на котором написано дополнительное название
CREATE TABLE Language_add_indicator(
	idLanguage INT AUTO_INCREMENT NOT NULL PRIMARY KEY, # ID языка
	Name_language VARCHAR(100) NOT NULL # Название языка
);

# Системы
CREATE TABLE Systems(
	idSystem INT AUTO_INCREMENT NOT NULL PRIMARY KEY, # ID системы
	Name_systems VARCHAR(500) NOT NULL# Название системы
);

# Оборудование, на котором проводится методика
CREATE TABLE Equipment(
	idEquipment INT AUTO_INCREMENT NOT NULL PRIMARY KEY, # ID оборудования
	Name_equipment VARCHAR(500) NOT NULL # Название оборудования
);

# Методика измерения показателя
CREATE TABLE Method(
	idMethod INT AUTO_INCREMENT NOT NULL PRIMARY KEY, # ID методики
	Name_method_Russian VARCHAR(500) NOT NULL, # Название методики на русском
	Name_method_foreign VARCHAR(500), # Название методики на иностранном
	Conditions_method TEXT(10000), # Условия проведения методики
	Restrictions_method TEXT(10000), # Ограничения при проведении методики
	Normal_value_method FLOAT, # Условно нормальное значение
	Borderline_value_method VARCHAR(25), # Граничные значения
	idSource_method INT, # ID источника порядка проведения методики
	Other_information TEXT(10000), # Другая полезная информация
	FOREIGN KEY (idSource_method) REFERENCES Source_method(idSource_method) 
);

# Оборудование, которое используется при проведении методики
CREATE TABLE Unit_method_equip(
	idUnit_met_equip INT AUTO_INCREMENT NOT NULL PRIMARY KEY, # ID оборудования для методики
	idMethod INT, # ID методики
	idEquipment INT, # ID оборудования
	FOREIGN KEY (idMethod) REFERENCES Method(idMethod),
	FOREIGN KEY (idEquipment) REFERENCES Equipment(idEquipment)
);

# Базовое название показателя 
CREATE TABLE Basic_name_indicator(
	idBasicName INT AUTO_INCREMENT NOT NULL PRIMARY KEY, # ID базового названия
	Latin_name VARCHAR(500) NOT NULL, # Латинское название показателя
    Short_name VARCHAR(25) NOT NULL, # Краткое латинское название
	Unit_measure VARCHAR(100), # Единицы измерения
	Discription_basic TEXT(10000), # Описание показателя
	idSystem INT NOT NULL, # ID системы
	idType_indicator INT NOT NULL, # ID типа показателя: первичный или вторичный
	FOREIGN KEY (idSystem) REFERENCES Systems(idSystem),
	FOREIGN KEY (idType_indicator) REFERENCES Type_indicator(idType_indicator)
);

# Формула для расчёта показателя
CREATE TABLE Formula(
	idFormula INT AUTO_INCREMENT NOT NULL PRIMARY KEY, # ID формулы
	Calculation_form TEXT(10000) NOT NULL, # Формула расчёта
	Normal_value_form FLOAT, # Условно нормальное значение
	Borderline_value_form VARCHAR(25) # Граничные значения
);

# Связь формулы и базового имени (Один показатель может иметь несколько формул расчёта)
# Для вторичного типа базового имени показателя
CREATE TABLE Unit_form_basic(
	idUnit_form_basic INT AUTO_INCREMENT NOT NULL PRIMARY KEY, # ID связи формулы и базового названия
	idFormula INT, # ID формулы
	idBasicName INT, # ID базового имени
	FOREIGN KEY (idFormula) REFERENCES Formula(idFormula),
	FOREIGN KEY (idBasicName) REFERENCES Basic_name_indicator(idBasicName)
);

# Формируемые показатели по методике
# Для первичного типа базового имени показателя
CREATE TABLE Formed_idicator_method(
	idFormed_indicator INT AUTO_INCREMENT NOT NULL PRIMARY KEY, # ID формируемых показателей
	idMethod INT, # ID методики
	idBasicName INT, # ID базового имени
	FOREIGN KEY (idMethod) REFERENCES Method(idMethod),
	FOREIGN KEY (idBasicName) REFERENCES Basic_name_indicator(idBasicName)
);

# Дополнительное название показателя
CREATE TABLE Additional_name(
	idAddName INT AUTO_INCREMENT NOT NULL PRIMARY KEY, # ID доплнительного названия
	Abbreviation_add_name VARCHAR(25) NOT NULL, # Аббревиатрура
	Decoding_abbrev VARCHAR(500) NOT NULL, # Расшифровка аббревиатуры
	idLanguage INT NOT NULL, # ID языка описания
	idBasicName INT NOT NULL, # ID базового имени
	FOREIGN KEY (idLanguage) REFERENCES Language_add_indicator(idLanguage),
	FOREIGN KEY (idBasicName) REFERENCES Basic_name_indicator(idBasicName)
);

# Связь источника и доп.имени
CREATE TABLE Unite_lit_addname(
	idUnit_lit_addname INT AUTO_INCREMENT NOT NULL PRIMARY KEY, # ID связи доп.имени и источника
	idLiteratures INT, # ID литературного источника
	idAddName INT, # ID дополнительного имени
	FOREIGN KEY (idLiteratures) REFERENCES Literatures(idLiteratures),
	FOREIGN KEY (idAddName) REFERENCES Additional_name(idAddName)
);