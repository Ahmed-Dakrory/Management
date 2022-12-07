from django import template
from django.utils.safestring import mark_safe
from mainApp.models import *
from django.db import connection
register = template.Library()


@register.simple_tag
def get_in_by_fac_data(category,size,day_to_generate):
    # print(day_to_generate)
    col = size
    row = category
    
    
    with connection.cursor() as cursorLast:
        try:
            day_to_generate = datetime.strptime(day_to_generate, '%d/%m/%Y')
            sql_query = """
                SELECT count(*) FROM management.transaction 
                left join item on transaction.item_id=item.id
                left join size on item.size_id=size.id
                left join category on item.category_id=category.id
                where category.id="""+str(row.id)+""" and size.id = """+str(col.id)+""" and ( type_of_transaction_id="""+str(settings.ID_ADD_TYPE_OF_TRANSACTION)+""" )
                and DATE_FORMAT(STR_TO_DATE(`item`.`created`, '%Y-%m-%d'), '%d-%m') = DATE_FORMAT(STR_TO_DATE('"""+str(day_to_generate.year)+"""-"""+str(day_to_generate.month)+"""-"""+str(day_to_generate.day)+"""','%Y-%m-%d'), '%d-%m')

            """
            # print(sql_query)
            cursorLast.execute(sql_query)
            cursorAllData = cursorLast.fetchone()
            in_items=cursorAllData[0]
        except:
            in_items = 0

    return in_items


@register.simple_tag
def get_in_by_company_data(category,size,day_to_generate):
    # print(day_to_generate)
    col = size
    row = category
    
    
    with connection.cursor() as cursorLast:
        try:
            day_to_generate = datetime.strptime(day_to_generate, '%d/%m/%Y')
            sql_query = """
                SELECT count(*) FROM management.transaction 
                left join item on transaction.item_id=item.id
                left join size on item.size_id=size.id
                left join category on item.category_id=category.id
                where category.id="""+str(row.id)+""" and transaction.company_id is not null and size.id = """+str(col.id)+""" and ( type_of_transaction_id="""+str(settings.ID_RETURN_TYPE_OF_TRANSACTION)+""")
                and DATE_FORMAT(STR_TO_DATE(`item`.`created`, '%Y-%m-%d'), '%d-%m') = DATE_FORMAT(STR_TO_DATE('"""+str(day_to_generate.year)+"""-"""+str(day_to_generate.month)+"""-"""+str(day_to_generate.day)+"""','%Y-%m-%d'), '%d-%m')

            """
            print(sql_query)
            cursorLast.execute(sql_query)
            cursorAllData = cursorLast.fetchone()
            in_items=cursorAllData[0]
        except:
            in_items = 0

    return in_items




@register.simple_tag
def get_in_by_rep_data(category,size,day_to_generate):
    # print(day_to_generate)
    col = size
    row = category
    
    
    with connection.cursor() as cursorLast:
        try:
            day_to_generate = datetime.strptime(day_to_generate, '%d/%m/%Y')
            sql_query = """
                SELECT count(*) FROM management.transaction 
                left join item on transaction.item_id=item.id
                left join size on item.size_id=size.id
                left join category on item.category_id=category.id
                where category.id="""+str(row.id)+""" and transaction.representitive_id is not null and size.id = """+str(col.id)+""" and ( type_of_transaction_id="""+str(settings.ID_RETURN_TYPE_OF_TRANSACTION)+""")
                and DATE_FORMAT(STR_TO_DATE(`item`.`created`, '%Y-%m-%d'), '%d-%m') = DATE_FORMAT(STR_TO_DATE('"""+str(day_to_generate.year)+"""-"""+str(day_to_generate.month)+"""-"""+str(day_to_generate.day)+"""','%Y-%m-%d'), '%d-%m')

            """
            # print(sql_query)
            cursorLast.execute(sql_query)
            cursorAllData = cursorLast.fetchone()
            in_items=cursorAllData[0]
        except:
            in_items = 0

    return in_items



@register.simple_tag
def get_out_by_rep_data(category,size,day_to_generate):
    # print(day_to_generate)
    col = size
    row = category
    
    with connection.cursor() as cursorLast:
        try:
            day_to_generate = datetime.strptime(day_to_generate, '%d/%m/%Y')
            sql_query = """
                SELECT count(*) FROM management.transaction 
                left join item on transaction.item_id=item.id
                left join size on item.size_id=size.id
                left join category on item.category_id=category.id
                where category.id="""+str(row.id)+""" and transaction.representitive_id is not null and size.id = """+str(col.id)+""" and ( type_of_transaction_id="""+str(settings.ID_OUT_TYPE_OF_TRANSACTION)+""")
                and DATE_FORMAT(STR_TO_DATE(`item`.`created`, '%Y-%m-%d'), '%d-%m') = DATE_FORMAT(STR_TO_DATE('"""+str(day_to_generate.year)+"""-"""+str(day_to_generate.month)+"""-"""+str(day_to_generate.day)+"""','%Y-%m-%d'), '%d-%m')

            """
            # print(sql_query)
            cursorLast.execute(sql_query)
            cursorAllData = cursorLast.fetchone()
            out_items=cursorAllData[0]
        except:
            out_items = 0

    return out_items



@register.simple_tag
def get_out_by_comp_data(category,size,day_to_generate):
    # print(day_to_generate)
    col = size
    row = category
    
    with connection.cursor() as cursorLast:
        try:
            day_to_generate = datetime.strptime(day_to_generate, '%d/%m/%Y')
            sql_query = """
                SELECT count(*) FROM management.transaction 
                left join item on transaction.item_id=item.id
                left join size on item.size_id=size.id
                left join category on item.category_id=category.id
                where category.id="""+str(row.id)+""" and transaction.company_id is not null and size.id = """+str(col.id)+""" and ( type_of_transaction_id="""+str(settings.ID_OUT_TYPE_OF_TRANSACTION)+""")
                and DATE_FORMAT(STR_TO_DATE(`item`.`created`, '%Y-%m-%d'), '%d-%m') = DATE_FORMAT(STR_TO_DATE('"""+str(day_to_generate.year)+"""-"""+str(day_to_generate.month)+"""-"""+str(day_to_generate.day)+"""','%Y-%m-%d'), '%d-%m')

            """
            # print(sql_query)
            cursorLast.execute(sql_query)
            cursorAllData = cursorLast.fetchone()
            out_items=cursorAllData[0]
        except:
            out_items = 0

    return out_items




@register.simple_tag
def get_total_by_data(category,size,day_to_generate):
    # print(day_to_generate)
    col = size
    row = category
    
    with connection.cursor() as cursorLast:
        try:
            day_to_generate = datetime.strptime(day_to_generate, '%d/%m/%Y')
            sql_query = """
                SELECT count(*) FROM management.transaction 
                left join item on transaction.item_id=item.id
                left join size on item.size_id=size.id
                left join category on item.category_id=category.id
                where category.id="""+str(row.id)+""" and size.id = """+str(col.id)+""" and ( type_of_transaction_id="""+str(settings.ID_ADD_TYPE_OF_TRANSACTION)+"""  or type_of_transaction_id="""+str(settings.ID_RETURN_TYPE_OF_TRANSACTION)+""")
                and DATE_FORMAT(STR_TO_DATE(`item`.`created`, '%Y-%m-%d'), '%d-%m') = DATE_FORMAT(STR_TO_DATE('"""+str(day_to_generate.year)+"""-"""+str(day_to_generate.month)+"""-"""+str(day_to_generate.day)+"""','%Y-%m-%d'), '%d-%m')

            """
            # print(sql_query)
            cursorLast.execute(sql_query)
            cursorAllData = cursorLast.fetchone()
            in_items=cursorAllData[0]
        except:
            in_items = 0
        # print(in_items)
        try:
            sql_query = """
                SELECT count(*) FROM management.transaction 
                left join item on transaction.item_id=item.id
                left join size on item.size_id=size.id
                left join category on item.category_id=category.id
                where category.id="""+str(row.id)+""" and size.id = """+str(col.id)+""" and ( type_of_transaction_id="""+str(settings.ID_OUT_TYPE_OF_TRANSACTION)+""")
                and DATE_FORMAT(STR_TO_DATE(`item`.`created`, '%Y-%m-%d'), '%d-%m') = DATE_FORMAT(STR_TO_DATE('"""+str(day_to_generate.year)+"""-"""+str(day_to_generate.month)+"""-"""+str(day_to_generate.day)+"""','%Y-%m-%d'), '%d-%m')

            """
            # print(sql_query)
            cursorLast.execute(sql_query)
            cursorAllData = cursorLast.fetchone()
            out_items=cursorAllData[0]
        except:
            out_items = 0

    
        # except:
        #     pass
            
    return in_items - out_items


@register.simple_tag
def get_remain_data(category,size):
    total_items = item.objects.filter( Q(category__id=category.id) & Q(size__id=size.id) & Q(exists=True) & Q(deleted_date=None)).count()
    return total_items

@register.simple_tag
def get_total_remain_data(category):
    total_items = item.objects.filter( Q(category__id=category.id) & Q(exists=True) & Q(deleted_date=None)).count()
    return total_items



