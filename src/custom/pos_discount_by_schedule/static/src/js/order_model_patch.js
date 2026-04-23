/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { Order, Orderline } from "@point_of_sale/app/store/models";

patch(Order.prototype, {
    add_product(product, options) {
        super.add_product(product, options);
        
        this.apply_time_discount();
    },

    apply_time_discount() {
        const now = new Date();
        const currentHour = now.getHours() + (now.getMinutes() / 60.0);
        
        // Las reglas estarán en this.pos.discount_rules
        const rules = this.pos.discount_rules || [];
        
        // Buscamos la regla activa según la hora
        const rule = rules.find(r => currentHour >= r.hour_from && currentHour < r.hour_to);
        
        if (rule) {
            this.get_orderlines().forEach(line => {
            console.log("Paso");
                // Aplicamos el descuento de la regla
                if (rule.is_exclusive) {
                    console.log("Prueba if");
                    line.set_discount(rule.discount_percentage);
                } else if (line.get_discount() === 0) {
                    console.log("Prueba else");
                    line.set_discount(rule.discount_percentage);
                }
            });
        }
    }
});

// Evitar que el cajero cambie el descuento si la regla es exclusiva
patch(Orderline.prototype, {
    set_discount(discount) {
        const now = new Date();
        const currentHour = now.getHours() + (now.getMinutes() / 60.0);
        const rules = this.pos.discount_rules || [];
        const rule = rules.find(r => currentHour >= r.hour_from && currentHour < r.hour_to);

        // Si la regla es exclusiva, ignoramos lo que el cajero teclee
        // y forzamos el descuento de nuestra regla.
        if (rule && rule.is_exclusive) {
            this.pos.env.services.notification.add(
                `La regla "${rule.name}" es exclusiva. No se pueden aplicar otros descuentos.`,
                {
                    type: "warning",
                    title: "Descuento bloqueado",
                    sticky: false,
                }
            );
            return super.set_discount(rule.discount_percentage);
        }

        // Si no hay regla exclusiva, permitimos el descuento manual
        return super.set_discount(discount);
    }
});
