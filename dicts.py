status_WH_dict = {
    "availability-confirmed": {
        "status_name": "Заброньте плз",
        "status_WH_state": False
    },
    "billed": {
        "status_name": "Получены данные об оплате LP",
        "status_WH_state": False
    },
    "refund": {
        "status_name": "Средства возвращены, скидка 10% на след покупку предложена.",
        "status_WH_state": True
    },
    "go-receive-it": {
        "status_name": "Товар в транзите на НП",
        "status_WH_state": True
    },
    "brand-reminded-18days": {
        "status_name": "Напоминание поставщику отправлено через 15 дней",
        "status_WH_state": True
    },
    "offline-ok": {
        "status_name": "Покупатель в магазине доволен",
        "status_WH_state": True
    },
    "brand-reminded-7days": {
        "status_name": "Напоминание поставщику отправлено через 8 дней",
        "status_WH_state": True
    },
    "waiting-for-refund": {
        "status_name": "Товар получен, покупатель ждет возврата средств",
        "status_WH_state": True
    },
    "sent-back": {
        "status_name": "Товар отправлен на возврат (внести номер накладной)",
        "status_WH_state": True
    },
    "back-in-stock-notification": {
        "status_name": "Покупатель уведомлен о наличии",
        "status_WH_state": False
    },
    "waiting-notification": {
        "status_name": "Покупатель ждет уведомления о наличии",
        "status_WH_state": False
    },
    "date-change-refund": {
        "status_name": "Дата поступления изменилась: отмена заказа",
        "status_WH_state": True
    },
    "date-change-ok": {
        "status_name": "Дата поступления изменилась: согласовано с покупателем",
        "status_WH_state": True
    },
    "brand-reminded-11days": {
        "status_name": "Напоминание поставщику отправлено через 11 дней",
        "status_WH_state": True
    },
    "brand-reminded-4days": {
        "status_name": "Напоминание поставщику отправлено через 4 дня",
        "status_WH_state": True
    },
    "preorder-received": {
        "status_name": "Предзаказ поступил на склад",
        "status_WH_state": True
    },
    "sent-to-brand-21days": {
        "status_name": "Предзаказ отправлен поставщику: 21 день",
        "status_WH_state": True
    },
    "sent-to-brand-14days": {
        "status_name": "Предзаказ отправлен поставщику: 14 дней",
        "status_WH_state": True
    },
    "sent-to-brand-10days": {
        "status_name": "Предзаказ отправлен поставщику: 10 дней",
        "status_WH_state": True
    },
    "sent-to-brand-7days": {
        "status_name": "Предзаказ отправлен поставщику: 7 дней",
        "status_WH_state": True
    },
    "sent-to-brand-3days": {
        "status_name": "Предзаказ отправлен поставщику: 3 дня",
        "status_WH_state": True
    },
    "preorder-21days": {
        "status_name": "Cогласован предзаказ с оплатой: 21 день",
        "status_WH_state": False
    },
    "preorder-14days": {
        "status_name": "Cогласован предзаказ с оплатой: 14 дней",
        "status_WH_state": False
    },
    "preorder-10days": {
        "status_name": "Cогласован предзаказ с оплатой: 10 дней",
        "status_WH_state": False
    },
    "preorder-3days": {
        "status_name": "Согласован предзаказ с оплатой: 3 дня",
        "status_WH_state": False
    },
    "cancel-other": {
        "status_name": "Отменен",
        "status_WH_state": False
    },
    "billing-did-not-suit": {
        "status_name": "Заказ перемещается между складами",
        "status_WH_state": False
    },
    "prepayed": {
        "status_name": "Оплата поступила",
        "status_WH_state": True
    },
    "redirect": {
        "status_name": "Доставка перенесена",
        "status_WH_state": True
    },
    "client-confirmed": {
        "status_name": "К отправке по внешнему ТТН",
        "status_WH_state": False
    },
    "assembling-complete": {
        "status_name": "Укомплектован",
        "status_WH_state": True
    },
    "delivering": {
        "status_name": "Передано службе доставки",
        "status_WH_state": True
    },
    "assembling": {
        "status_name": "Нужно отправить в перемещении",
        "status_WH_state": False
    },
    "not-in-stock": {
        "status_name": "Нет в наличии: проверка наличия альтернативы",
        "status_WH_state": False
    },
    "send-to-assembling": {
        "status_name": "Перемещается",
        "status_WH_state": False
    },
    "complete": {
        "status_name": "Выполнен",
        "status_WH_state": True
    },
    "no-call": {
        "status_name": "Не смогли связаться",
        "status_WH_state": False
    },
    "send-to-delivery": {
        "status_name": "Передан в доставку",
        "status_WH_state": True
    },
    "new": {
        "status_name": "Проверка наличия",
        "status_WH_state": False
    },
    "refund-ok": {
        "status_name": "Покупатель доволен возвратом",
        "status_WH_state": True
    },
    "payment-notification": {
        "status_name": "Напоминание об оплате отправлено",
        "status_WH_state": False
    },
    "payment-didnt-come-trough": {
        "status_name": "Оплата не поступила",
        "status_WH_state": False
    },
    "waiting-for-shipment": {
        "status_name": "ТТН создана / ждет передачи перевозчику",
        "status_WH_state": True
    },
    "preorder-check": {
        "status_name": "Проверка возможности предзаказа",
        "status_WH_state": False
    },
    "booked-for-10d": {
        "status_name": "Долгосрочная бронь (10 дней)",
        "status_WH_state": False
    },
    "booked-for-7d": {
        "status_name": "Долгосрочная бронь (7 дней)",
        "status_WH_state": False
    },
    "booked-for-3d": {
        "status_name": "Долгосрочная бронь (3 дня)",
        "status_WH_state": False
    },
    "booked-till-payed": {
        "status_name": "Забронирован до оплаты",
        "status_WH_state": False
    },
    "paid-reserve-pending": {
        "status_name": "Заброньте плз (оплачено)",
        "status_WH_state": False
    },
    "paid-and-booked": {
        "status_name": "Оплачен и забронен до отправки",
        "status_WH_state": True
    },
    "paid-problem": {
        "status_name": "Проблема комплектации (оплачено)",
        "status_WH_state": False
    },
    "new-paid": {
        "status_name": "Проверка (оплачено)",
        "status_WH_state": False
    },
    "returns": {
        "status_name": "Проблема в комплектации",
        "status_WH_state": False
    },
    "booking-failed": {
        "status_name": "Бронь оплачена",
        "status_WH_state": False
    },
    "new-payment-pending": {
        "status_name": "Ждет оплаты (новый)",
        "status_WH_state": False
    },
    "online-ok": {
        "status_name": "Заказ оплачен и готов к выдаче",
        "status_WH_state": True
    },
    "preorder-7days": {
        "status_name": "Cогласован предзаказ с оплатой: 7 дней",
        "status_WH_state": False
    },
    "problem-gone": {
        "status_name": "Проблема покупателя решена (внести комментарий - как)",
        "status_WH_state": True
    },
    "troubleshooting": {
        "status_name": "Согласование решения проблемы с руководителем",
        "status_WH_state": True
    },
    "4days-not-accepted": {
        "status_name": "Товар не получен в течение 4х дней",
        "status_WH_state": True
    },
    "problem": {
        "status_name": "Покупатель не доволен (внести комментарий)",
        "status_WH_state": True
    },
    "billed-with-discount": {
        "status_name": "Реквизиты со скидкой за ожидание согласованы",
        "status_WH_state": False}
    }

cols_to_drop = ['bonusesCreditTotal',
                'bonusesChargeTotal',
                'orderType',
                'expired',
                'managerId',
                'contact',
                'currency',
                'customerComment',
                'managerComment',
                'length',
                'width',
                'height',
                'weight',
                'patronymic',
                'additionalPhone',
                'ready_steady_go',
                'no_notifications_mode',
                'shipping_details',
                'how_to_communicate',
                'gift_receiving_person',
                'cards_texts',
                'deadline_preorder']

shipmentStores = {'000000003':'U8_Odesa',
                  '000000007':'SDD',
                  'sdd_main' :'slashdotdash_shopify',
                  '000000012':'U8_Kh_temp',
                  '000000001':'U8_Kharkiv',
                  '000000009':'U8_Dropship',
                  '000000010':'U8_Preorders',
                  '000000011':'U8_Transit'}

new_order_no_WH = ['Дата оплати',
              'Кількість по CRM загалом',
              'Кількість по Fin загалом',
              'Замовлення в не обох списках',
              'Сума по CRM загалом',
              'Сума по Fin загалом',
              'Cписок по CRM загалом',
              'Cписок по Fin загалом',
              'Загалом по SDD -  Fondy СТЕРІНА в CRM',
              'Список замовлень по SDD -  Fondy СТЕРІНА в CRM',
              'Кількість замовлень по SDD -  Fondy СТЕРІНА в CRM',
              'Загалом по SDD - На карту СТЕРИНА в CRM',
              'Список замовлень по SDD - На карту СТЕРИНА в CRM',
              'Кількість замовлень по SDD - На карту СТЕРИНА в CRM',
              'Загалом по SDD - СТЕРИНА LP в CRM',
              'Список замовлень по SDD - СТЕРИНА LP в CRM',
              'Кількість замовлень по SDD - СТЕРИНА LP в CRM',
              'Загалом по SDD - Наложенный платеж Марченко в CRM',
              'Список замовлень по SDD - Наложенный платеж Марченко в CRM',
              'Кількість замовлень по SDD - Наложенный платеж Марченко в CRM',
              'Загалом по SDD - Не фискализируемый в CRM',
              'Список замовлень по SDD - Не фискализируемый в CRM',
              'Кількість замовлень по SDD - Не фискализируемый в CRM',
              'Загалом по SDD - Наличными СТЕРИНА в CRM',
              'Список замовлень по SDD - Наличными СТЕРИНА в CRM',
              'Кількість замовлень по SDD - Наличными СТЕРИНА в CRM',
              'Загалом по Безнал прямые оплаты в Fin',
              'Список замовлень по Безнал прямые оплаты в Fin',
              'Кількість замовлень по Безнал прямые оплаты в Fin',
              'Загалом по Карта Бурововой в Fin',
              'Список замовлень по Карта Бурововой в Fin',
              'Кількість замовлень по Карта Бурововой в Fin',
              'Загалом по Касса SDD Одесса  в Fin',
              'Список замовлень по Касса SDD Одесса  в Fin',
              'Кількість замовлень по Касса SDD Одесса  в Fin',
              'Загалом по Безнал терминал в Fin',
              'Список замовлень по Безнал терминал в Fin',
              'Кількість замовлень по Безнал терминал в Fin',
              'Загалом по Сейф SDD Одесса  в Fin',
              'Список замовлень по Сейф SDD Одесса  в Fin',
              'Кількість замовлень по Сейф SDD Одесса  в Fin',
              'Загалом по Баланс у Новій Пошті в Fin',
              'Список замовлень по Баланс у Новій Пошті в Fin',
              'Кількість замовлень по Баланс у Новій Пошті в Fin',
              'Загалом по Післяплати в Fin', 'Список замовлень по Післяплати в Fin',
              'Кількість замовлень по Післяплати в Fin', 'Загалом по Касса USD в Fin',
              'Список замовлень по Касса USD в Fin',
              'Кількість замовлень по Касса USD в Fin']



new_order_with_WH = ['Дата оплати',
              'Кількість замовлень в обл. тов.',
              'Кількість по CRM загалом',
              'Кількість по Fin загалом',
              'Замовлення в не обох списках',
              'Сума по CRM загалом',
              'Сума по Fin загалом',
              'Сумма за обл. тов.',
              'Cписок по CRM загалом',
              'Cписок по Fin загалом',
              'Список айді CRM (за обл. тов.)',
              'Загалом по SDD -  Fondy СТЕРІНА в CRM',
              'Список замовлень по SDD -  Fondy СТЕРІНА в CRM',
              'Кількість замовлень по SDD -  Fondy СТЕРІНА в CRM',
              'Загалом по SDD - На карту СТЕРИНА в CRM',
              'Список замовлень по SDD - На карту СТЕРИНА в CRM',
              'Кількість замовлень по SDD - На карту СТЕРИНА в CRM',
              'Загалом по SDD - СТЕРИНА LP в CRM',
              'Список замовлень по SDD - СТЕРИНА LP в CRM',
              'Кількість замовлень по SDD - СТЕРИНА LP в CRM',
              'Загалом по SDD - Наложенный платеж Марченко в CRM',
              'Список замовлень по SDD - Наложенный платеж Марченко в CRM',
              'Кількість замовлень по SDD - Наложенный платеж Марченко в CRM',
              'Загалом по SDD - Не фискализируемый в CRM',
              'Список замовлень по SDD - Не фискализируемый в CRM',
              'Кількість замовлень по SDD - Не фискализируемый в CRM',
              'Загалом по SDD - Наличными СТЕРИНА в CRM',
              'Список замовлень по SDD - Наличными СТЕРИНА в CRM',
              'Кількість замовлень по SDD - Наличными СТЕРИНА в CRM',
              'Загалом по Безнал прямые оплаты в Fin',
              'Список замовлень по Безнал прямые оплаты в Fin',
              'Кількість замовлень по Безнал прямые оплаты в Fin',
              'Загалом по Карта Бурововой в Fin',
              'Список замовлень по Карта Бурововой в Fin',
              'Кількість замовлень по Карта Бурововой в Fin',
              'Загалом по Касса SDD Одесса  в Fin',
              'Список замовлень по Касса SDD Одесса  в Fin',
              'Кількість замовлень по Касса SDD Одесса  в Fin',
              'Загалом по Безнал терминал в Fin',
              'Список замовлень по Безнал терминал в Fin',
              'Кількість замовлень по Безнал терминал в Fin',
              'Загалом по Сейф SDD Одесса  в Fin',
              'Список замовлень по Сейф SDD Одесса  в Fin',
              'Кількість замовлень по Сейф SDD Одесса  в Fin',
              'Загалом по Баланс у Новій Пошті в Fin',
              'Список замовлень по Баланс у Новій Пошті в Fin',
              'Кількість замовлень по Баланс у Новій Пошті в Fin',
              'Загалом по Післяплати в Fin', 'Список замовлень по Післяплати в Fin',
              'Кількість замовлень по Післяплати в Fin', 'Загалом по Касса USD в Fin',
              'Список замовлень по Касса USD в Fin',
              'Кількість замовлень по Касса USD в Fin']

cols_to_show_status_comparison = ['Код CRM', 'Проведен?', 'status_WH', 'Сумма', 'totalSumm', 'clean_order_number', 'Номер', 'Розбіжність по сумі', 'Розбіжність по статусу','status_name', 'Статус заказа']