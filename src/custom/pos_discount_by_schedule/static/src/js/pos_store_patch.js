/** @odoo-module **/
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";

patch(PosStore.prototype, {
    async _processData(data) {
        await super._processData(...arguments);
        // Aquí capturamos lo que viene del backend (Python)
        this.discount_rules = data['pos.discount.rule'] || [];
    },
});
