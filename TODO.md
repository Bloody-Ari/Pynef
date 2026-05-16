# TODO - Ajuste setup_design_tab (pynef_gui)

- [ ] Revisar `pynef_gui.py` completo para ubicar/ajustar `setup_design_tab` y `update_nozzle()`
- [ ] Modificar `setup_design_tab` para que muestre SOLO: diámetro de cámara, Ac/At y Ae/At (equivalente a `py_input_example.py`)
- [ ] Implementar función de cálculo (en `NozzleDesignerGUI`) que replique exactamente:
  - `chamber_area = pi * (r^2)`
  - `throat_radius` desde `Ac/At`
  - `exit_radius` desde `Ae/At`
  - `chamber_cone_length` y `exit_cone_length` con tan(15°) usando `0.26794919243`
- [ ] Actualizar `update_nozzle()` para usar los inputs y calcular parámetros derivados antes de llamar a `pynef.updateNozzle()`
- [ ] Ajustar labels/variables tk para coherencia (diámetro vs radio)
- [ ] Ejecutar `pynef_gui.py` y validar que al presionar “Actualizar Nozzle” se recalculan radios/longitudes correctamente

