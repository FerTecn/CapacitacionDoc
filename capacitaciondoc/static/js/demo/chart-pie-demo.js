function crearGraficaPastel(canvasId, data) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  
  new Chart(ctx, {
      type: 'doughnut',
      data: {
          labels: data.map(opcion => `Opción ${opcion.opcion}`),
          datasets: [{
              data: data.map(opcion => opcion.count),
              label: 'Personas',
              backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(153, 102, 255, 0.2)'
              ],
              borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)'
              ],
              borderWidth: 1
          }]
      },
  });
}

document.addEventListener('DOMContentLoaded', function() {
  // Graficas del instructor
  crearGraficaPastel('chartInstructor1', resultados.instructor1);
  crearGraficaPastel('chartInstructor2', resultados.instructor2);
  crearGraficaPastel('chartInstructor3', resultados.instructor3);
  crearGraficaPastel('chartInstructor4', resultados.instructor4);
  crearGraficaPastel('chartInstructor5', resultados.instructor5);
  crearGraficaPastel('chartInstructor6', resultados.instructor6);
  crearGraficaPastel('chartInstructor7', resultados.instructor7);

  // Graficas del material
  crearGraficaPastel('chartMaterial1', resultados.material1);
  crearGraficaPastel('chartMaterial2', resultados.material2);
  crearGraficaPastel('chartMaterial3', resultados.material3);

  // Graficas del curso
  crearGraficaPastel('chartCurso1', resultados.curso1);
  crearGraficaPastel('chartCurso2', resultados.curso2);
  crearGraficaPastel('chartCurso3', resultados.curso3);
  crearGraficaPastel('chartCurso4', resultados.curso4);

  // Graficas de infraestructura
  crearGraficaPastel('chartInfraestructura1', resultados.insfraestructura1);
  crearGraficaPastel('chartInfraestructura2', resultados.insfraestructura2);
  crearGraficaPastel('chartInfraestructura3', resultados.insfraestructura3);
  crearGraficaPastel('chartInfraestructura4', resultados.insfraestructura4);
  crearGraficaPastel('chartInfraestructura5', resultados.insfraestructura5);
  crearGraficaPastel('chartInfraestructura6', resultados.insfraestructura6);
});