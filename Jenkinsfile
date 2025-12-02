pipeline {
    agent {
        kubernetes {
            label 'buildkit'
            defaultContainer 'buildkit'
            yaml """
                apiVersion: v1
                kind: Pod
                metadata:
                  labels:
                    jenkins/label: buildkit
                spec:
                  containers:
                    # BuildKit daemon + client
                    - name: buildkit
                      image: moby/buildkit:latest
                      securityContext:
                        privileged: true
                      command:
                        - buildkitd
                      args:
                        - --addr
                        - unix:///run/buildkit/buildkitd.sock
                      volumeMounts:
                        - name: docker-config
                          mountPath: /root/.docker/config.json
                          subPath: .dockerconfigjson
                        - name: workspace-volume
                          mountPath: /home/jenkins/agent

                    # Jenkins agent (jnlp)
                    - name: jnlp
                      image: jenkins/inbound-agent:latest
                      volumeMounts:
                        - name: workspace-volume
                          mountPath: /home/jenkins/agent

                    # kubectl for deployment
                    - name: kubectl
                      image: bitnami/kubectl:latest
                      command: ["sleep"]
                      args: ["infinity"]
                      volumeMounts:
                        - name: workspace-volume
                          mountPath: /home/jenkins/agent

                  volumes:
                    - name: docker-config
                      secret:
                        secretName: ghcr-secret
                    - name: workspace-volume
                      emptyDir: {}
            """
        }
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    // Global variables definition
    environment {
        REGISTRY = "ghcr.io"
        IMAGE = "henrardb/jdccabanga"
    }

    stages {
        // --- CHECKOUT ---
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Git') {
            steps {
                container('buildkit') {
                    sh """
                        git config --global --add safe.directory \"${WORKSPACE}\"
                    """
                }
            }
        }

        stage('Compute Build Metadata') {
            steps {
                container('buildkit') {
                    script {
                        env.DATE_TAG = sh(script: "date +%Y%m%d%H%M%S", returnStdout: true).trim()
                        env.COMMIT   = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                        env.TAG      = "${env.DATE_TAG}-${env.COMMIT}"
                    }
                }
            }
        }

        stage('Build & Push with BuildKit') {
            steps {
                container('buildkit') {
                    sh """
                        buildctl build \
                          --frontend=dockerfile.v0 \
                          --opt platform=linux/amd64,linux/arm64 \
                          --local context=. \
                          --local dockerfile=. \
                          --output type=image,name=${env.REGISTRY}/${env.IMAGE}:${env.TAG},push=true \
                          --output type=image,name=${env.REGISTRY}/${env.IMAGE}:latest,push=true
                    """
                }
            }
        }

        // --- KUBERNETES DEPLOYMENT ---
        stage('Deploy to K3s') {
            steps {
               withCredentials([file(credentialsId: 'kubeconfig-k3s', variable: 'KUBECONFIG')]){
                    container('kubectl') {
                        sh """
                            export KUBECONFIG=\$KUBECONFIG
                            kubectl -n jdccabanga set image cronjob/jdccabanga \
                                jdccabanga=${env.REGISTRY}/${env.IMAGE}:${env.TAG}
                            kubectl -n jdccabanga create job --from=cronjob/jdccabanga jdccabanga-${env.DATE_TAG}
                        """
                    }
               }
            }
        }
    }
}