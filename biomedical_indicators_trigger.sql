USE biomedical_indicators; # подключаемся к базе
drop trigger if exists typ_ind; # удаляем триггер если он был

# для начала написания триггера
DELIMITER // 
# создаём триггер, который реагирует после добавления записи в таблицу Basic_name_indicator
CREATE TRIGGER typ_ind AFTER insert on Basic_name_indicator FOR EACH ROW 
BEGIN
	# idType_indicator последней добавленой записи
	select idType_indicator from Basic_name_indicator order by idBasicName DESC limit 1 into @a; 
	if @a=1 then # если равен 1 (первичный)
		# выбираем последний добавленный idBasicName, в котором idType_indicator равен 1
		select idBasicName from Basic_name_indicator where idType_indicator=@a order by idBasicName DESC limit 1 into @r;
		insert into formed_idicator_method(idBasicName) values(@r); # добавляем в таблицу формируемых показателей по методике
	ELSEIF @a=2 then # если равен 2 (вторичный)
		# выбираем последний добавленный idBasicName, в котором idType_indicator равен 2
		select idBasicName from Basic_name_indicator where idType_indicator=@a order by idBasicName DESC limit 1 into @r1;
		insert into Unit_form_basic(idBasicName) values(@r1); # добавляем в таблицу связи формулы и базового имени
	end if;
END //