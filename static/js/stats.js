import Chart from 'chart.js/auto';
import Litepicker from 'litepicker';

const picker = new Litepicker({ 
    element: document.getElementById('f-filter-date-input'),
    lang: 'es',
    numberOfMonths: 2,
    numberOfColumns: 2,
    singleMode: false,
    switchingMonths: 1,
    tooltipText: {
        one: 'dia',
        other: 'dias'
    },
    tooltipNumber: (totalDays) => {
        return totalDays - 1;
    }
});

/************************** ON PAGE LOAD **************************/

// Configure Date Picker
window.addEventListener('load', () => {
    // Select current week
    var now = new Date();
    var today = swcms.newDate(new Date(now.getFullYear(), now.getMonth(), now.getDate()))
    var firstDayOfWeek = today.getFirstDayOfWeekDate();

    picker.setDateRange(firstDayOfWeek, today);

    var ctx = document.getElementById('graph-stats--visits');
    var ctxe = document.getElementById('graph-stats--extern');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Orientación general', 'Atención psicológica', 'Asistencia legal', 'Apoyo Social', 'Gestión de casos', 'No prestó ningún servicio', 'Otro'],
            datasets: [{
                label:"cantidad",
                data: [12, 19, 3, 15, 2, 9, 5],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 132, 112, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(255, 132, 112, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    var myChart2 = new Chart(ctxe, {
        type: 'bar',
        data: {
            labels: ['Policía', 'Ministerio Público', 'SESAL', 'Secretaría de Relaciones exteriores y Cooperación Internacional', 'DINAF', 'Albergue', 'ONG', 'Otro'],
            datasets: [{
                label:"cantidad",
                data: [5, 11, 3, 12, 2, 19, 5, 1],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 132, 112, 0.2)',
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(255, 132, 112, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
