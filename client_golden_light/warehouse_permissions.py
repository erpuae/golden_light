import frappe

def se_list_permission(data):
    """
    Permission to filter Stock Entry list
    """
    
    user = ""
    wh_condition = ""
    warehouses = ()
    if not user:
        user = frappe.session.user
    if not user == "Administrator":
        whs = frappe.db.sql("""SELECT tup.for_value,tup.allow FROM `tabUser Permission` tup
                JOIN `tabWarehouse` tw on tw.name = tup.for_value 
                WHERE tup.user = '{0}' and ((tup.allow = 'Warehouse' and tup.apply_to_all_doctypes = 1) || 
                (tup.allow = 'Warehouse' and tup.apply_to_all_doctypes = 0 and tup.applicable_for = 'Stock Entry'))""".format(user),as_dict=1)

        for w in whs:
            warehouses += (w['for_value'],)
        warehouse = ""
        if len(whs) == 1:
            warehouse = " = '{}'".format(whs[0]['for_value'])
        else:
            warehouse = "in {}".format(warehouses)

        wh_condition = """`tabStock Entry`.name in 
                            (SELECT parent FROM `tabStock Entry Detail`
                            WHERE t_warehouse {0} || s_warehouse {0} )""".format(warehouse)
        owner_exception = "`tabStock Entry`.owner = '{0}'".format(user)

    if warehouses:
        data = """({0} || {1})""".format(owner_exception, wh_condition)
        return data


@frappe.whitelist()
def permitted_warehouse(company=None):
    warehouse = []
    admin = 0
    user = frappe.session.user
    roles = [r.role for r in frappe.get_all(
        "Has Role",
        filters={"parent": user},
        fields=["role"]
    )]
    whs = frappe.db.sql("""select for_value from `tabUser Permission`
                           where allow = "Warehouse" and user = '%s'""" %(user),as_dict=1)
    if user == "Administrator" or "System Manager" in roles:
        warehouse = frappe.db.get_list('Warehouse',{'company':company},pluck='name')
    else:
        for w in whs:
            warehouse.append(w['for_value'])
    return warehouse
    

