import os
import sys
import tempfile
import unittest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import MagicMock

# Asegurar que la carpeta source esté en sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SOURCE_DIR = os.path.join(ROOT_DIR, "source")
if SOURCE_DIR not in sys.path:
    sys.path.insert(0, SOURCE_DIR)

import flet as ft
import openpyxl
from Negocio.Controlador.ControladorReportes import ControladorReportes
from Presentacion.PantallaReportes import PantallaReportes


class DummyPage:
    """Mock ligero de ft.Page para pruebas de UI sin servidor gráfico."""
    def __init__(self):
        self.overlay = []
        self.snack_bar = None
        self.theme_mode = ft.ThemeMode.LIGHT
        self.updated = False

    def update(self):
        self.updated = True


class MockReporteRepository:
    """Repositorio simulado con datos poblados para los 10 tipos de reporte."""
    def __init__(self, vacio=False, lanzar_error=False):
        self.vacio = vacio
        self.lanzar_error = lanzar_error

    def _check(self, datos):
        if self.lanzar_error:
            raise RuntimeError("Fallo simulado de conexión a base de datos")
        return [] if self.vacio else datos

    def obtener_asistencia_completa(self, fecha_inicio, fecha_fin, tipo_usuario=None):
        ahora = datetime.now()
        return self._check([
            {
                "identificador": "ALU-1001",
                "nombre_completo": "Carlos Lopez Hernandez",
                "tipo_usuario": "ALUMNO",
                "fecha_entrada": ahora - timedelta(hours=3),
                "fecha_salida": ahora - timedelta(hours=1),
                "estado": "FINALIZADO",
                "tiempo_estadia": timedelta(hours=2),
                "grupo": "A",
                "semestre": "1",
                "nombre_carrera": "Ingenieria en desarrollo y tecnologias de Software",
                "nombre_facultad": "Facultad de Ingenieria",
                "nombre_institucion": None,
            },
            {
                "identificador": "PLZ-5001",
                "nombre_completo": "Jorge Ramirez Diaz",
                "tipo_usuario": "PERSONAL",
                "fecha_entrada": ahora - timedelta(hours=4),
                "fecha_salida": None,
                "estado": "ACTIVO",
                "tiempo_estadia": timedelta(hours=4),
                "grupo": None,
                "semestre": None,
                "nombre_carrera": None,
                "nombre_facultad": None,
                "nombre_institucion": None,
            },
        ])

    def obtener_usuarios_mas_activos(self, fecha_inicio, fecha_fin, tipo_usuario=None):
        return self._check([
            {
                "identificador": "ALU-1001",
                "nombre_completo": "Carlos Lopez Hernandez",
                "tipo_usuario": "ALUMNO",
                "visitas": 3,
                "segundos_totales": 28800,
                "promedio_segundos": 9600,
                "horas_totales": 8.0,
                "promedio_horas": 2.67,
                "ultima_visita": datetime.now(),
            },
            {
                "identificador": "ALU-1002",
                "nombre_completo": "Maria Gomez Perez",
                "tipo_usuario": "ALUMNO",
                "visitas": 2,
                "segundos_totales": 14400,
                "promedio_segundos": 7200,
                "horas_totales": 4.0,
                "promedio_horas": 2.0,
                "ultima_visita": datetime.now(),
            },
        ])

    def obtener_horas_pico_avanzado(self, fecha_inicio, fecha_fin):
        return self._check([
            {"hora": 9, "total": 5, "alumnos": 3, "personal": 1, "visitantes": 1},
            {"hora": 11, "total": 8, "alumnos": 6, "personal": 1, "visitantes": 1},
        ])

    def obtener_tendencia_diaria(self, fecha_inicio, fecha_fin, tipo_usuario=None):
        return self._check([
            {
                "fecha": date.today() - timedelta(days=1),
                "total_usuarios": 4,
                "alumnos": 2,
                "personal": 1,
                "visitantes": 1,
            },
            {
                "fecha": date.today(),
                "total_usuarios": 6,
                "alumnos": 4,
                "personal": 1,
                "visitantes": 1,
            },
        ])

    def obtener_reporte_carreras(self, fecha_inicio, fecha_fin):
        return self._check([
            {
                "carrera": "Ingenieria en desarrollo y tecnologias de Software",
                "total_visitas": 5,
                "usuarios_unicos": 2,
                "promedio_horas": Decimal("2.50"),
            },
            {
                "carrera": "Contaduria Publica",
                "total_visitas": 3,
                "usuarios_unicos": 1,
                "promedio_horas": Decimal("1.80"),
            },
        ])

    def obtener_reporte_facultades(self, fecha_inicio, fecha_fin):
        return self._check([
            {
                "facultad": "Facultad de Ingenieria",
                "total_visitas": 5,
                "usuarios_unicos": 2,
                "promedio_horas": Decimal("2.50"),
            },
            {
                "facultad": "Facultad de Contaduria y Administracion",
                "total_visitas": 3,
                "usuarios_unicos": 1,
                "promedio_horas": Decimal("1.80"),
            },
        ])

    def obtener_reporte_semestres(self, fecha_inicio, fecha_fin):
        return self._check([
            {
                "semestre": "1",
                "total_visitas": 7,
                "usuarios_unicos": 2,
                "promedio_horas": Decimal("2.30"),
            }
        ])

    def obtener_visitantes_externos(self, fecha_inicio, fecha_fin):
        return self._check([
            {
                "institucion": "Universidad Autonoma de Chiapas",
                "total_visitas": 2,
                "usuarios_unicos": 1,
                "promedio_horas": Decimal("1.50"),
            }
        ])

    def obtener_reporte_saturacion(self, fecha_inicio, fecha_fin):
        return self._check([
            {"hora": 10, "total_usuarios": 9, "alumnos": 7, "personal": 1, "visitantes": 1},
            {"hora": 12, "total_usuarios": 4, "alumnos": 3, "personal": 1, "visitantes": 0},
        ])

    def obtener_reporte_crecimiento(self):
        return self._check([
            {
                "mes": datetime.now().strftime("%Y-%m"),
                "total_visitas": 12,
                "usuarios_unicos": 4,
                "alumnos": 8,
                "personal": 2,
                "visitantes": 2,
            }
        ])


TIPOS_REPORTE = [
    "Asistencia completa",
    "Usuarios más activos",
    "Horas pico avanzado",
    "Tendencia diaria",
    "Reporte por carrera",
    "Reporte por facultad",
    "Reporte por semestre",
    "Visitantes externos",
    "Reporte de saturación",
    "Reporte de crecimiento",
]


class TestReportes(unittest.TestCase):

    def test_01_importacion_e_instanciacion(self):
        """Verifica que ControladorReportes y PantallaReportes se importen e instancien sin errores."""
        repo_mock = MockReporteRepository()
        controlador = ControladorReportes(repo=repo_mock)
        self.assertIsNotNone(controlador)
        self.assertIs(controlador.repo, repo_mock)

        page = DummyPage()
        pantalla = PantallaReportes(page, controlador=controlador)
        self.assertIsNotNone(pantalla)
        self.assertEqual(pantalla.fecha_fin, datetime.now().strftime("%Y-%m-%d"))
        self.assertNotEqual(pantalla.fecha_inicio, "2026-05-01")
        self.assertNotEqual(pantalla.fecha_fin, "2026-05-31")

        # Verificar que NO exista FilePicker en page.overlay (evita error "Unknown control: FilePicker")
        tiene_file_picker = any(isinstance(ctrl, ft.FilePicker) for ctrl in page.overlay)
        self.assertFalse(tiene_file_picker, "No debe existir ft.FilePicker en page.overlay")
        self.assertFalse(hasattr(pantalla, "file_picker"), "No debe existir atributo file_picker en PantallaReportes")

        # Verificar colores semánticos para modo claro/oscuro
        self.assertEqual(pantalla.CARD, "surface")
        self.assertEqual(pantalla.TEXT, "onSurface")
        self.assertEqual(pantalla.TEXT_SECONDARY, "onSurfaceVariant")

    def test_02_diez_reportes_con_datos_poblados(self):
        """Verifica que los 10 tipos de reporte procesen y grafiquen datos poblados correctamente."""
        repo_mock = MockReporteRepository(vacio=False)
        controlador = ControladorReportes(repo=repo_mock)
        page = DummyPage()
        pantalla = PantallaReportes(page, controlador=controlador)

        for tipo in TIPOS_REPORTE:
            with self.subTest(tipo=tipo):
                datos = controlador.generar_reporte(
                    tipo=tipo,
                    fecha_inicio=pantalla.fecha_inicio,
                    fecha_fin=pantalla.fecha_fin,
                    tipo_usuario="Todos",
                )
                self.assertTrue(len(datos) > 0, f"El reporte '{tipo}' debe devolver datos")

                pantalla.tipo_reporte_dd.value = tipo
                pantalla.actualizar(None)

                # Verificar que se hayan creado cards, gráfica visual (Container) y tabla
                self.assertTrue(len(pantalla.cards_row.controls) > 0)
                self.assertIsInstance(
                    pantalla.chart_container.content,
                    ft.Container,
                    f"El reporte '{tipo}' debe generar una gráfica visual en un ft.Container",
                )
                self.assertIsInstance(
                    pantalla.distribution_container.content,
                    ft.Container,
                    f"El reporte '{tipo}' debe generar una tabla en distribution_container",
                )

    def test_03_diez_reportes_con_listas_vacias(self):
        """Verifica que los 10 tipos de reporte soporten listas vacías sin lanzar ValueError ni ZeroDivisionError."""
        repo_vacio = MockReporteRepository(vacio=True)
        controlador = ControladorReportes(repo=repo_vacio)
        page = DummyPage()
        pantalla = PantallaReportes(page, controlador=controlador)

        for tipo in TIPOS_REPORTE:
            with self.subTest(tipo=tipo):
                datos = controlador.generar_reporte(
                    tipo=tipo,
                    fecha_inicio=pantalla.fecha_inicio,
                    fecha_fin=pantalla.fecha_fin,
                )
                self.assertEqual(datos, [])

                pantalla.tipo_reporte_dd.value = tipo
                pantalla.actualizar(None)

                # También probar llamada directa a generar_grafica con lista vacía
                grafica = pantalla.generar_grafica(tipo, [])
                self.assertIsNotNone(grafica)

        # Probar directamente todos los métodos render_* con lista vacía (incluyendo render_saturacion)
        pantalla.render_asistencia([])
        pantalla.render_usuarios_activos([])
        pantalla.render_horas_pico([])
        pantalla.render_tendencia([])
        pantalla.render_carreras([])
        pantalla.render_facultades([])
        pantalla.render_semestres([])
        pantalla.render_visitantes([])
        pantalla.render_saturacion([])
        pantalla.render_crecimiento([])

    def test_04_manejo_excepciones_repositorio(self):
        """Verifica que fallos de conexión en el repositorio sean capturados de forma segura."""
        repo_error = MockReporteRepository(lanzar_error=True)
        controlador = ControladorReportes(repo=repo_error)

        for tipo in TIPOS_REPORTE:
            with self.subTest(tipo=tipo):
                resultado = controlador.generar_reporte(
                    tipo=tipo,
                    fecha_inicio="2026-01-01",
                    fecha_fin="2026-12-31",
                )
                self.assertEqual(resultado, [])

        with tempfile.TemporaryDirectory() as tmpdir:
            ruta_fallida = os.path.join(tmpdir, "fallo.xlsx")
            exito = controlador.exportar_excel(
                ruta=ruta_fallida,
                tipo="Asistencia completa",
                fecha_inicio="2026-01-01",
                fecha_fin="2026-12-31",
            )
            self.assertFalse(exito)

    def test_05_exportacion_excel_todos_los_reportes(self):
        """Verifica que la exportación a Excel (.xlsx) exporte exactamente las columnas y filas de la tabla de la derecha."""
        from unittest.mock import patch

        repo_mock = MockReporteRepository(vacio=False)
        controlador = ControladorReportes(repo=repo_mock)
        page = DummyPage()
        pantalla = PantallaReportes(page, controlador=controlador)

        with tempfile.TemporaryDirectory() as tmpdir:
            for tipo in TIPOS_REPORTE:
                with self.subTest(tipo=tipo):
                    nombre_archivo = f"test_{tipo.lower().replace(' ', '_')}.xlsx"
                    ruta_xlsx = os.path.join(tmpdir, nombre_archivo)

                    pantalla.tipo_reporte_dd.value = tipo
                    pantalla.actualizar(None)

                    # Verificar que las columnas y filas de la tabla actual estén pobladas
                    self.assertTrue(len(pantalla.columnas_actuales) > 0)
                    self.assertTrue(len(pantalla.filas_actuales) > 0)

                    # Simular selección de ruta en el diálogo de guardado de tkinter
                    with patch("tkinter.Tk"), patch("tkinter.filedialog.asksaveasfilename", return_value=ruta_xlsx):
                        resultado = pantalla.exportar_excel(None)

                    self.assertTrue(resultado, f"Debe exportar correctamente el reporte '{tipo}'")
                    self.assertTrue(os.path.exists(ruta_xlsx), f"Debe existir el archivo {ruta_xlsx}")

                    wb = openpyxl.load_workbook(ruta_xlsx)
                    ws = wb["Reporte"]

                    # Verificar que los encabezados del Excel coincidan exactamente con columnas_actuales de la tabla
                    encabezados_excel = [cell.value for cell in ws[1]]
                    self.assertEqual(encabezados_excel, pantalla.columnas_actuales)
                    self.assertTrue(ws[1][0].font.bold, "Los encabezados deben estar en negrita")

                    # Verificar que la cantidad de filas coincida con filas_actuales + 1 (encabezado)
                    self.assertEqual(ws.max_row, len(pantalla.filas_actuales) + 1)
                    wb.close()

            # Con repositorio vacío debe limpiar columnas_actuales/filas_actuales y retornar False
            controlador_vacio = ControladorReportes(repo=MockReporteRepository(vacio=True))
            pantalla_vacia = PantallaReportes(DummyPage(), controlador=controlador_vacio)
            self.assertEqual(pantalla_vacia.columnas_actuales, [])
            self.assertEqual(pantalla_vacia.filas_actuales, [])
            ruta_vacia = os.path.join(tmpdir, "vacio.xlsx")
            self.assertFalse(pantalla_vacia.exportar_excel(ruta=ruta_vacia))
            self.assertFalse(
                controlador_vacio.exportar_excel(ruta=ruta_vacia, tipo="Asistencia completa")
            )

    def test_06_integracion_base_de_datos_postgresql(self):
        """Verifica que ControladorReportes y PantallaReportes funcionen con ReporteRepositoryImpl conectado a biblioteca_cds."""
        from Persistencia.Postgres.Pool.DBPool import db

        # Asegurar de forma idempotente que existan registros de prueba recientes en biblioteca_cds
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) AS total FROM Registro WHERE fecha_entrada >= NOW() - INTERVAL '30 days'")
                row = cur.fetchone()
                total_recientes = row["total"] if isinstance(row, dict) else row[0]

                if total_recientes == 0:
                    cur.execute("""
                        INSERT INTO Usuario (id_usuario, nombre, ap_paterno, ap_materno, fecha_nacimiento, tipo_usuario, identificador)
                        VALUES
                            (1, 'Carlos', 'Lopez', 'Hernandez', '2002-05-10', 'ALUMNO', 'ALU-1001'),
                            (2, 'Maria', 'Gomez', 'Perez', '2001-08-15', 'ALUMNO', 'ALU-1002'),
                            (3, 'Jorge', 'Ramirez', 'Diaz', '1985-03-20', 'PERSONAL', 'PLZ-5001'),
                            (4, 'Ana', 'Torres', 'Morales', '1998-11-02', 'VISITANTE', 'VIS-1')
                        ON CONFLICT (id_usuario) DO NOTHING;

                        INSERT INTO Alumno (id_usuario, matricula, id_grupo)
                        VALUES (1, 'ALU-1001', 1), (2, 'ALU-1002', 27)
                        ON CONFLICT (id_usuario) DO NOTHING;

                        INSERT INTO Personal (id_usuario, n_plaza)
                        VALUES (3, 'PLZ-5001')
                        ON CONFLICT (id_usuario) DO NOTHING;

                        INSERT INTO Visitante (id_usuario, id_institucion)
                        VALUES (4, 1)
                        ON CONFLICT (id_usuario) DO NOTHING;

                        INSERT INTO Registro (fecha_entrada, fecha_salida, id_usuario) VALUES
                            (NOW() - INTERVAL '3 hours', NOW() - INTERVAL '1 hour', 1),
                            (NOW() - INTERVAL '5 hours', NOW() - INTERVAL '2 hours', 2),
                            (NOW() - INTERVAL '4 hours', NULL, 3),
                            (NOW() - INTERVAL '2 hours', NOW() - INTERVAL '30 minutes', 4),
                            (NOW() - INTERVAL '1 day' + INTERVAL '9 hours', NOW() - INTERVAL '1 day' + INTERVAL '12 hours', 1),
                            (NOW() - INTERVAL '2 days' + INTERVAL '10 hours', NOW() - INTERVAL '2 days' + INTERVAL '11 hours', 2),
                            (NOW() - INTERVAL '15 days' + INTERVAL '8 hours', NOW() - INTERVAL '15 days' + INTERVAL '11 hours', 1);
                    """)
                    conn.commit()

        controlador_real = ControladorReportes()
        page = DummyPage()
        pantalla_real = PantallaReportes(page, controlador=controlador_real)
        pantalla_real.fecha_inicio = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        pantalla_real.fecha_fin = datetime.now().strftime("%Y-%m-%d")

        for tipo in TIPOS_REPORTE:
            with self.subTest(tipo=tipo):
                datos = controlador_real.generar_reporte(
                    tipo=tipo,
                    fecha_inicio=pantalla_real.fecha_inicio,
                    fecha_fin=pantalla_real.fecha_fin,
                )
                self.assertIsInstance(datos, list)
                self.assertGreater(len(datos), 0, f"El reporte '{tipo}' en BD debe retornar registros de prueba")

                pantalla_real.tipo_reporte_dd.value = tipo
                pantalla_real.actualizar(None)
                self.assertIsInstance(pantalla_real.chart_container.content, ft.Container)


if __name__ == "__main__":
    unittest.main()
