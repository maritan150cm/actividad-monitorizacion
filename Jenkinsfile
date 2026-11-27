pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo '=== Etapa 1: Construyendo y verificando archivos del proyecto ==='
                sh 'ls -la'
                sh 'sleep 3'
            }
        }
        stage('Test') {
            steps {
                echo '=== Etapa 2: Ejecutando pruebas básicas de integridad ==='
                sh 'test -f app.py && test -f README.md'
                sh 'sleep 3'
            }
        }
        stage('Analyze') {
            steps {
                echo '=== Etapa 3: Análisis estático de seguridad (SAST) ==='
                sh 'grep -rn "DEBUG = True" app.py || echo "Sin modo debug expuesto"'
                sh 'sleep 3'
            }
        }
        stage('Deploy') {
            steps {
                echo '=== Etapa 4: Desplegando artefacto validado ==='
                echo 'Despliegue simulado completado exitosamente en entorno local'
                sh 'sleep 3'
            }
        }
    }
}
