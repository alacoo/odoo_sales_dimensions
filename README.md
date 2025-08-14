# Módulo `sale_dimensions`

Este módulo extiende la funcionalidad del módulo de **Ventas** de Odoo para añadir campos de dimensiones (**Largo**, **Ancho**, **Alto**) a las líneas de pedido de venta.

## Requisitos

- **Odoo:** Versión 18  
- **Módulos de Odoo requeridos:** Sales  
- **Python:** Versión 3.8 o superior  
- **Librerías Python:** No se requieren librerías externas adicionales, solo las dependencias estándar de Odoo.  
- **Docker y Docker Compose:** El entorno de desarrollo y las pruebas están diseñados para ejecutarse con Docker.  
  El proyecto incluye un `docker-compose.yml` que monta el módulo en la ruta de *addons* de Odoo.

## Instalación

1. Clona o descarga este repositorio y coloca el directorio `sale_dimensions` dentro de tu carpeta de *addons* mapeada al contenedor de Docker (ver `docker-compose.yml`).  
2. Asegúrate de que los contenedores de Odoo y PostgreSQL estén en ejecución. Si no lo están, levántalos con:
   ```bash
   docker compose up -d
3. Activa el Modo Desarrollador en Odoo: Ajustes > Activar el modo de desarrollador

4. Ve a Aplicaciones, haz clic en Actualizar lista de aplicaciones y busca sale_dimensions para instalarlo.

## Ejecución de pruebas

Para correr las pruebas del módulo desde tu terminal:

docker exec -it nombre_del_contenedor_web odoo -d nombre_de_la_base_de_datos -i nombre_del_modulo --test-enable --stop-after-init --xmlrpc-port=puerto


Ejemplo real:

docker exec -it odoo_pruebatecnica_delfix-web-1 odoo -d allan -i sale_dimensions --test-enable --stop-after-init --xmlrpc-port=8072



## Decisiones de diseño

Extensión de modelo: Se amplió sale.order.line para añadir x_length, x_width, x_height y uom_length. Las dimensiones se definen por línea de pedido.

Personalización de vista: Se heredaron vistas para mostrar los campos en el formulario de líneas de pedido y en la tabla del portal del cliente (sale.sale_order_portal_content).

Unidad de medida: Se creó uom_length como campo separado para permitir distintas unidades (m, cm, in) por línea.


## Screenshots
Formulario de SO con dimensiones:

![App Screenshot](https://yxxjbulijsfudmsepzdp.supabase.co/storage/v1/object/public/Personal/Screenshot%202025-08-14%20111301.png)

Preview de la venta:

![App Screenshot](https://yxxjbulijsfudmsepzdp.supabase.co/storage/v1/object/public/Personal/Screenshot%202025-08-14%20111758.png)

PDF generado:

![App Screenshot](https://yxxjbulijsfudmsepzdp.supabase.co/storage/v1/object/public/Personal/Screenshot%202025-08-14%20111828.png)

