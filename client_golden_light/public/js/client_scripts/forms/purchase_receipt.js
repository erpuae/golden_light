frappe.ui.form.on('Purchase Receipt', {
    refresh: filter_items,
    setup: filter_items,
    supplier: filter_items,
    onload_post_render: filter_items,
    // onload (frm) {
    //     filter_items(frm);
    //     setTimeout(() => {

    //         $(".form-links").hide();
    //     }, 10);
    // },
    // validate(frm) {
    //     validated = true;
    //     for (const item of frm.doc.items) {
    //         if(item.rate == 0) {
    //             validated = false;
    //             frappe.msgprint("Rate cannot be zero.");
    //         }
    //     }

    //     frappe.validated = validated;
    // },
});

function filter_items(frm) {
    frm.fields_dict.items.grid.get_field('item_code').get_query = function(doc, cdt, cdn) {

        if(!doc || !cdt || !cdn) {
            return
        }

        const row = locals[cdt][cdn];
        const filters = [
            ['has_variants', '=', 0]
        ];

        if (row.group)
            filters.push(['item_group', '=', row.group]);

        if (row.item_category)
            filters.push(['item_category', '=', row.item_category]);

        return { filters };
    };
}
