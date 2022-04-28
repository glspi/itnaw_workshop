node('jenkins-python') {
    stage('build') {
        container('python') {
            checkout scm
            sh 'python capthook/interface_updater.py'
        }
    }
}
