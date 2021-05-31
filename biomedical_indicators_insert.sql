use biomedical_indicators;
# Данные таблицы equipment
INSERT INTO equipment (Name_equipment) VALUES('Монометр');
INSERT INTO equipment (Name_equipment) VALUES('Газовый счётчик');
INSERT INTO equipment (Name_equipment) VALUES('Динамометр');
INSERT INTO equipment (Name_equipment) VALUES('Стабилометрическая платформа');
INSERT INTO equipment (Name_equipment) VALUES('Электромиограф');

# Данные таблицы method
INSERT INTO method (Name_method_Russian) VALUES('ЭКГ');
INSERT INTO method (Name_method_Russian) VALUES('Произвольная задержка дыхания');
INSERT INTO method (Name_method_Russian) VALUES('Спирография');
INSERT INTO method (Name_method_Russian) VALUES('Динамометрия');
INSERT INTO method (Name_method_Russian) VALUES('Стабилография');
INSERT INTO method (Name_method_Russian) VALUES('Миография');

# Данные таблицы unit_method_equip
INSERT INTO unit_method_equip (idMethod, idEquipment) VALUES(1, 1);
INSERT INTO unit_method_equip (idMethod, idEquipment) VALUES(3, 2);
INSERT INTO unit_method_equip (idMethod, idEquipment) VALUES(4, 3);
INSERT INTO unit_method_equip (idMethod, idEquipment) VALUES(5, 4);
INSERT INTO unit_method_equip (idMethod, idEquipment) VALUES(6, 5);

# Данные таблицы systems
INSERT INTO systems (Name_systems) VALUES('Общая система');
INSERT INTO systems (Name_systems) VALUES('Сердечно-сосудистая система');
INSERT INTO systems (Name_systems) VALUES('Дыхательная система');
INSERT INTO systems (Name_systems) VALUES('Костно-мышечная система');
INSERT INTO systems (Name_systems) VALUES('Нервная система');
INSERT INTO systems (Name_systems) VALUES('Система терморегуляции');

# Данные таблицы type_indicator
INSERT INTO type_indicator (Name_type_indicator) VALUES('Первичный');
INSERT INTO type_indicator (Name_type_indicator) VALUES('Вторичный');

# Данные таблицы basic_name_indicator
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Age', 'Ag',1, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Corpus pondus', 'CP', 1, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Statura', 'St', 1, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Corporis Longitudo', 'CL', 1, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Corpus superficiei', 'CP', 1, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Cor rate', 'CR', 2, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Systoles sanguinem pressura', 'SSP', 2, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Diastolic sanguinem pressura', 'DSP', 2, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Variatio range', 'VR', 2, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('R-R-intervalla', 'R-RI', 2, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Respiratorii volumine', 'RV', 3, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Respiratorii rate', 'RR', 3, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Duratio spiritus tenens', 'DST', 3, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Dolor nisl', 'DN', 3, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Carbo dioxide emissione', 'CDE', 3, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Maximum evacuatione pulmones', 'MEP', 3, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Subsidiis volumine inspiratione', 'SVI', 3, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Subsidiis expiratory volumine', 'SEV', 3, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Carbo dioxide contentus in fundus aeris', 'CDCA', 3, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Carbo dioxide contentus in alveolar caeli', 'CDCC', 3, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Pulmonis evacuatione', 'PE', 3, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Maximum musculus labore', 'MML', 4, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Maximum musculus patientia', 'MMP', 4, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Duratio motus boeoticus', 'DMB', 4, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Amplitudine musculus motus initio operis', 'AMMinitioO', 4, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Amplitudine musculus motus in fine operis', 'AMMinFO', 4, 1);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Kwaasa Index', 'KI', 2, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Myznikov Index', 'MI', 2, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Signum efficientiam operationem respiratorii', 'SEOR', NULL, NULL, 3, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Accentus campester', 'AC', 1, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Gradu corporis', 'GC', 1, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Corpus Massa Index', 'CMI', 1, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Erisman Vitae Index', 'EVI', 1, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Index eget mutationes', 'IEM', 1, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('In Calamo Index', 'INC', 1, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('In Robinson Index', 'IRI', 1, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Taxationem status autonomic nervosi', 'TSAN', 5, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Vane Index', 'VI', 5, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Systoles sanguinem volume', 'SSV', 1, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Index periphericis vascularium resistentia', 'IPVR', 2, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Periphericis vascularium resistentia', 'PVR', 2, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Ictum volumine sanguinem', 'IVS', 2, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Summa periphericis resistentia', 'SPR', 2, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Vitalis capacitatem pulmo', 'VCP', 3, 2);
INSERT INTO basic_name_indicator (Latin_name, Short_name, idSystem, idType_indicator) VALUES('Pulsus sanguinem pressura', 'PSP', 2, 2);

# Данные  таблицы formed_idicator_method
UPDATE formed_idicator_method SET idMethod = NULL WHERE idBasicName = 1;
UPDATE formed_idicator_method SET idMethod = NULL WHERE idBasicName = 2;
UPDATE formed_idicator_method SET idMethod = NULL WHERE idBasicName = 3;
UPDATE formed_idicator_method SET idMethod = NULL WHERE idBasicName = 4;
UPDATE formed_idicator_method SET idMethod = 1 WHERE idBasicName = 6;
UPDATE formed_idicator_method SET idMethod = 1 WHERE idBasicName = 7;
UPDATE formed_idicator_method SET idMethod = 1 WHERE idBasicName = 8;
UPDATE formed_idicator_method SET idMethod = 1 WHERE idBasicName = 10;
UPDATE formed_idicator_method SET idMethod = NULL WHERE idBasicName = 12;
UPDATE formed_idicator_method SET idMethod = 2 WHERE idBasicName = 13;
UPDATE formed_idicator_method SET idMethod = 3 WHERE idBasicName = 14;
UPDATE formed_idicator_method SET idMethod = 3 WHERE idBasicName = 15;
UPDATE formed_idicator_method SET idMethod = 3 WHERE idBasicName = 16;
UPDATE formed_idicator_method SET idMethod = 3 WHERE idBasicName = 17;
UPDATE formed_idicator_method SET idMethod = 3 WHERE idBasicName = 18;
UPDATE formed_idicator_method SET idMethod = 3 WHERE idBasicName = 19;
UPDATE formed_idicator_method SET idMethod = 3 WHERE idBasicName = 20;
UPDATE formed_idicator_method SET idMethod = 3 WHERE idBasicName = 21;
UPDATE formed_idicator_method SET idMethod = 4 WHERE idBasicName = 22;
UPDATE formed_idicator_method SET idMethod = 5 WHERE idBasicName = 23;
UPDATE formed_idicator_method SET idMethod = 6 WHERE idBasicName = 24;
UPDATE formed_idicator_method SET idMethod = 6 WHERE idBasicName = 25;
UPDATE formed_idicator_method SET idMethod = 6 WHERE idBasicName = 26;

# Данные таблицы formula
INSERT INTO formula (Calculation_form) VALUES('$ВР={{RR}_{\\max }}-{{RR}_{\\min }}$');
INSERT INTO formula (Calculation_form) VALUES('$ДО=\\frac{{{ДО}_{1}}-{{ДО}_{n}}}{n}$');
INSERT INTO formula (Calculation_form) VALUES('$КВ=\\frac{ЧСС\\times 10}{ПД}$');
INSERT INTO formula (Calculation_form) VALUES('$IM=\\frac{ЧСС\\times САД}{ДАД}$');
INSERT INTO formula (Calculation_form) VALUES('$ЭФдс=200-(121,36\\times ДО +3,546\\times ЧД)$');
INSERT INTO formula (Calculation_form) VALUES('$УрС={{МТ}^{0,4036}}\\times ЧСС \\times ПАД \\times 0,000126$');
INSERT INTO formula (Calculation_form) VALUES('$УФС=\\frac{700-3\\cdot ЧСС-2,5\\cdot СДД-2,7\\cdot В+0,28\\cdot МГ}{350-2,6\\cdot В+0,21\\cdot Р}$');
INSERT INTO formula (Calculation_form) VALUES('$ИМТ=\\frac{МТ}{{{ДТ}^{2}}}$');
INSERT INTO formula (Calculation_form) VALUES('$ЖИ=\\frac{ЖЕЛ}{МТ}$');
INSERT INTO formula (Calculation_form) VALUES('\\[ИФИ=0,01\\cdot (1,1\\cdot ЧСС+1,4\\cdot САД+0,8\\cdot ДАД+1,4\\cdot В+9\\cdot МТ-0,9\\cdot ДТ/100-27)\\]');
INSERT INTO formula (Calculation_form) VALUES('$РИ=0,75\\cdot (ЧСС+0,74\\cdot ПД)-72$');
INSERT INTO formula (Calculation_form) VALUES('$ИР=\\frac{ЧСС\\times САД}{100}$');
INSERT INTO formula (Calculation_form) VALUES('\\[УПС=\\frac{СДД\\times S}{ДМО}\\]');
INSERT INTO formula (Calculation_form) VALUES('\\[ИПСС=\\frac{СДД\\times 1330\\times 60}{МОК}\\]');
INSERT INTO formula (Calculation_form) VALUES('\\[ППС=\\frac{СДД\\times 1330\\times 60}{УО}\\]');
INSERT INTO formula (Calculation_form) VALUES('\\[УО=\\frac{ПД\\times 100}{\\left( ССА+ДАД \\right)/2}\\]');
INSERT INTO formula (Calculation_form) VALUES('$ОПС=\\frac{{{АД}_{ср}}\\times 1333\\times 60}{МОК}$');
INSERT INTO formula (Calculation_form) VALUES('$ПД=САД-ДАД$');
INSERT INTO formula (Calculation_form) VALUES('$S=71,84\\cdot {{МТ}^{0,425}}\\cdot {{Р}^{0,725}}$');
INSERT INTO formula (Calculation_form) VALUES('$СО=90,97+0,54\\cdot ПД-0,57\\cdot ДАД-0,61\\cdot В$');
INSERT INTO formula (Calculation_form) VALUES('$ИВ=\\frac{ЧСС\\times САД}{64}\\times \\left( 0,4\\times В+109 \\right)$');
INSERT INTO formula (Calculation_form) VALUES('$ВИК=\\left( 1-\\frac{ДАД}{ЧСС} \\right)\\times 100%$');
INSERT INTO formula (Calculation_form) VALUES('$ЖЕЛ=0,52\\cdot Р -0,022\\cdot В $');
INSERT INTO formula (Calculation_form) VALUES('\\[ЖЕЛ=ДО+РОвд+РОвыд\\]');

# Данные таблицы unit_form_basic
UPDATE unit_form_basic SET idFormula = 19 WHERE idBasicName = 5;
UPDATE unit_form_basic SET idFormula = 1 WHERE idBasicName = 9;
UPDATE unit_form_basic SET idFormula = 2 WHERE idBasicName = 11;
UPDATE unit_form_basic SET idFormula = 3 WHERE idBasicName = 27;
UPDATE unit_form_basic SET idFormula = 4 WHERE idBasicName = 28;
UPDATE unit_form_basic SET idFormula = 5 WHERE idBasicName = 29;
UPDATE unit_form_basic SET idFormula = 6 WHERE idBasicName = 30;
UPDATE unit_form_basic SET idFormula = 7 WHERE idBasicName = 31;
UPDATE unit_form_basic SET idFormula = 8 WHERE idBasicName = 32;
UPDATE unit_form_basic SET idFormula = 9 WHERE idBasicName = 33;
UPDATE unit_form_basic SET idFormula = 10 WHERE idBasicName = 34;
UPDATE unit_form_basic SET idFormula = 11 WHERE idBasicName = 35;
UPDATE unit_form_basic SET idFormula = 12 WHERE idBasicName = 36;
UPDATE unit_form_basic SET idFormula = 22 WHERE idBasicName = 37;
UPDATE unit_form_basic SET idFormula = 21 WHERE idBasicName = 38;
UPDATE unit_form_basic SET idFormula = 20 WHERE idBasicName = 39;
UPDATE unit_form_basic SET idFormula = 13 WHERE idBasicName = 40;
UPDATE unit_form_basic SET idFormula = 14 WHERE idBasicName = 41;
UPDATE unit_form_basic SET idFormula = 15 WHERE idBasicName = 42;
UPDATE unit_form_basic SET idFormula = 16 WHERE idBasicName = 43;
UPDATE unit_form_basic SET idFormula = 17 WHERE idBasicName = 44;
UPDATE unit_form_basic SET idFormula = 23 WHERE idBasicName = 45;
UPDATE unit_form_basic SET idFormula = 18 WHERE idBasicName = 46;
INSERT INTO unit_form_basic (idFormula, idBasicName) VALUES(24, 45);

# Данные таблицы `language_add_indicator`
INSERT INTO language_add_indicator (Name_language) VALUES('Русский');
INSERT INTO language_add_indicator (Name_language) VALUES('Английский');

# Данные таблицы `additional_name`
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('В', 'Возраст', 1, 1);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('МТ', 'Масса тела', 1, 2);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('Р', 'Рост', 1, 3);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ДТ', 'Длина тела', 1, 4);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('S', 'Площадь поверхности тела', 1, 5);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ЧСС', 'Частота сердечных сокращений', 1, 6);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('САД', 'Систолическое артериальное давление', 1, 7);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ДАД', 'Диастолическое артериальное давление', 1, 8);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ВР', 'Вариационный размах', 1, 9);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('RR', 'R-R-интервалы', 1, 10);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ДО', 'Дыхательный объём', 1, 11);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ЧД', 'Частота дыхания', 1, 12);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ПЗД', 'Продолжительность задержки дыхания', 1, 13);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('КПО2', 'Потребление кислорода', 1, 14);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('КСО2', 'Выделение углекислого газа', 1, 15);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('МВЛ', 'Максимальная вентиляция лёгких', 1, 16);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('РОвд', 'Резервный объем вдоха', 1, 17);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('РОвыд', 'Резервный объем выдоха', 1, 18);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('СО2Е', 'Содержание углекислоты в выдыхаемом воздухе', 1, 19);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('СО2А', 'Содержание углекислоты в альвеолярном воздухе', 1, 20);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ЛВ', 'Легочная вентиляция', 1, 21);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ММУ', 'Максимальное мышечное усилие', 1, 22);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ММВ', 'Максимальная мышечная выносливость', 1, 23);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('Т', 'Длительность стереотипных движений', 1, 24);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('Ан', 'Амплитуда мышечного движения в начале работы', 1, 25);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('Ак', 'Амплитуда мышечного движения в конце работы', 1, 26);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('КВ', 'Индекс Квааса', 1, 27);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('IМ', 'Индекс Мызникова', 1, 28);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ЭФдс', 'Показатель экономичности функционирования дыхательной системы', 1, 29);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('УрС', 'Уровень стресса', 1, 30);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('УФС', 'Уровень физического состояни', 1, 31);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ИМТ', 'Индекс массы тела', 1, 32);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ЖИ', 'Жизненный индекс Эрисмана', 1, 33);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ИФИ', 'Индекс функциональных изменений', 1, 34);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('РИ', 'Индекс Рида', 1, 35);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ИР', 'Индекс Робинсона', 1, 36);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ВИК', 'Оценка состояния вегетативной нервной системы', 1, 37);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ИВ', 'Индекс Вейна', 1, 38);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('СО', 'Систолический объем крови', 1, 39);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('УПС', 'Удельное периферическое сопротивление', 1, 40);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ИПСС', 'Индекс периферического сопротивления сосудов', 1, 41);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ПСС', 'Периферическоео сопротивление сосудов', 1, 42);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('УО', 'Ударный объем крови', 1, 43);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ОПС', 'Общее периферическое сопротивление', 1, 44);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ЖЕЛ', 'Жизненная емкость легких', 1, 45);
INSERT INTO additional_name (Abbreviation_add_name, Decoding_abbrev, idLanguage, idBasicName) VALUES('ПД', 'Пульсовое артериальное давление', 1, 46);