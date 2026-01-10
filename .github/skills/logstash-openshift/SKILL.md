---
name: logstash-openshift
description: Manage Logstash pipelines deployed in OpenShift using ConfigMaps. Use for pipeline configuration, deployment, troubleshooting, and maintenance of Logstash in containerized OpenShift environments.
---

# Logstash on OpenShift

Guide for managing Logstash pipelines in OpenShift using ConfigMap-based configuration management.

## Architecture Overview

### Deployment Pattern
- **Logstash Pods**: Run as Deployments or StatefulSets in OpenShift
- **Pipeline Configuration**: Stored in ConfigMaps
- **Secrets**: Sensitive credentials (passwords, API keys) stored in OpenShift Secrets
- **Persistent Storage**: Optional PVCs for file-based plugins or dead letter queues

### Typical Structure
```
ConfigMap: logstash-pipeline
  ├── input.conf    (Input plugins configuration)
  ├── filter.conf   (Filter/transformation logic)
  └── output.conf   (Output destinations)

ConfigMap: logstash-patterns (optional)
  └── custom.patterns (Grok patterns)

Secret: logstash-credentials
  ├── elasticsearch-password
  ├── kafka-keystore
  └── api-tokens
```

## ConfigMap Management

### Creating Pipeline ConfigMap

```bash
# Create from local files
oc create configmap logstash-pipeline \
  --from-file=input.conf \
  --from-file=filter.conf \
  --from-file=output.conf \
  -n <namespace>

# Create from YAML manifest
cat <<EOF | oc apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: logstash-pipeline
  namespace: logging
data:
  input.conf: |
    input {
      beats {
        port => 5044
      }
      kafka {
        bootstrap_servers => "kafka-cluster:9092"
        topics => ["logs"]
        codec => json
      }
    }
  
  filter.conf: |
    filter {
      if [type] == "syslog" {
        grok {
          match => { "message" => "%{SYSLOGLINE}" }
        }
        date {
          match => [ "timestamp", "MMM dd HH:mm:ss" ]
        }
      }
      
      # Remove fields
      mutate {
        remove_field => ["@version", "host"]
      }
    }
  
  output.conf: |
    output {
      elasticsearch {
        hosts => ["https://elasticsearch:9200"]
        index => "logstash-%{[@metadata][beat]}-%{+YYYY.MM.dd}"
        user => "\${ELASTICSEARCH_USER}"
        password => "\${ELASTICSEARCH_PASSWORD}"
        ssl => true
        cacert => "/etc/logstash/certs/ca.crt"
      }
      
      # Dead letter queue for failed events
      if "_grokparsefailure" in [tags] {
        file {
          path => "/var/log/logstash/failed-%{+YYYY-MM-dd}.log"
          codec => json_lines
        }
      }
    }
EOF
```

### Updating Pipeline Configuration

```bash
# Edit ConfigMap directly
oc edit configmap logstash-pipeline -n <namespace>

# Update from file
oc create configmap logstash-pipeline \
  --from-file=filter.conf \
  --dry-run=client -o yaml | oc apply -f -

# Patch specific key
oc patch configmap logstash-pipeline -n <namespace> \
  --type merge \
  -p '{"data":{"filter.conf":"<new-content>"}}'
```

### Reloading Configuration

Logstash supports automatic config reload, but for OpenShift:

```bash
# Force pod restart to pick up new ConfigMap
oc rollout restart deployment/logstash -n <namespace>

# Or delete pods to trigger recreation
oc delete pod -l app=logstash -n <namespace>

# Watch rollout status
oc rollout status deployment/logstash -n <namespace> --watch
```

## Deployment Configuration

### Logstash Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: logstash
  namespace: logging
spec:
  replicas: 2
  selector:
    matchLabels:
      app: logstash
  template:
    metadata:
      labels:
        app: logstash
    spec:
      containers:
      - name: logstash
        image: docker.elastic.co/logstash/logstash:8.11.0
        ports:
        - containerPort: 5044
          name: beats
          protocol: TCP
        - containerPort: 9600
          name: http
          protocol: TCP
        env:
        - name: ELASTICSEARCH_USER
          valueFrom:
            secretKeyRef:
              name: logstash-credentials
              key: elasticsearch-user
        - name: ELASTICSEARCH_PASSWORD
          valueFrom:
            secretKeyRef:
              name: logstash-credentials
              key: elasticsearch-password
        - name: LS_JAVA_OPTS
          value: "-Xmx1g -Xms1g"
        - name: PIPELINE_WORKERS
          value: "2"
        - name: PIPELINE_BATCH_SIZE
          value: "125"
        resources:
          requests:
            memory: "1.5Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        volumeMounts:
        - name: pipeline-config
          mountPath: /usr/share/logstash/pipeline
          readOnly: true
        - name: logstash-config
          mountPath: /usr/share/logstash/config/logstash.yml
          subPath: logstash.yml
          readOnly: true
        - name: patterns
          mountPath: /usr/share/logstash/patterns
          readOnly: true
        - name: certs
          mountPath: /etc/logstash/certs
          readOnly: true
        livenessProbe:
          httpGet:
            path: /
            port: 9600
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /
            port: 9600
          initialDelaySeconds: 30
          periodSeconds: 10
      volumes:
      - name: pipeline-config
        configMap:
          name: logstash-pipeline
      - name: logstash-config
        configMap:
          name: logstash-config
      - name: patterns
        configMap:
          name: logstash-patterns
          optional: true
      - name: certs
        secret:
          secretName: elasticsearch-certs
```

### Main Configuration (logstash.yml)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: logstash-config
  namespace: logging
data:
  logstash.yml: |
    http.host: "0.0.0.0"
    path.config: /usr/share/logstash/pipeline/*.conf
    config.reload.automatic: true
    config.reload.interval: 30s
    
    # Performance tuning
    pipeline.workers: 2
    pipeline.batch.size: 125
    pipeline.batch.delay: 50
    
    # Monitoring
    monitoring.enabled: false
    
    # Dead letter queue
    dead_letter_queue.enable: true
    dead_letter_queue.max_bytes: 1gb
    
    # Logging
    log.level: info
    path.logs: /usr/share/logstash/logs
```

## Pipeline Development Best Practices

### Input Configuration

```ruby
input {
  # Beats input for log shippers
  beats {
    port => 5044
    ssl => true
    ssl_certificate => "/etc/logstash/certs/server.crt"
    ssl_key => "/etc/logstash/certs/server.key"
  }
  
  # Kafka for high-throughput scenarios
  kafka {
    bootstrap_servers => "${KAFKA_BROKERS}"
    topics => ["application-logs", "system-logs"]
    group_id => "logstash-consumer"
    consumer_threads => 2
    codec => json
    auto_offset_reset => "latest"
  }
  
  # HTTP input for webhooks
  http {
    port => 8080
    codec => json
  }
}
```

### Filter Configuration

```ruby
filter {
  # Parse JSON if string
  if [message] =~ /^\{.*\}$/ {
    json {
      source => "message"
      target => "parsed"
    }
  }
  
  # Grok parsing for unstructured logs
  grok {
    match => { 
      "message" => [
        "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}",
        "%{SYSLOGLINE}"
      ]
    }
    tag_on_failure => ["_grokparsefailure"]
  }
  
  # Date parsing
  date {
    match => [ "timestamp", "ISO8601", "yyyy-MM-dd HH:mm:ss" ]
    target => "@timestamp"
  }
  
  # Enrich with Kubernetes metadata
  if [kubernetes] {
    mutate {
      add_field => {
        "namespace" => "%{[kubernetes][namespace]}"
        "pod" => "%{[kubernetes][pod_name]}"
        "container" => "%{[kubernetes][container_name]}"
      }
    }
  }
  
  # Conditional processing
  if [level] == "ERROR" or [level] == "FATAL" {
    mutate {
      add_tag => ["alert"]
      add_field => { "severity" => "high" }
    }
  }
  
  # Drop debug logs in production
  if [level] == "DEBUG" and [environment] == "production" {
    drop { }
  }
  
  # Clean up
  mutate {
    remove_field => ["@version", "host", "agent"]
  }
}
```

### Output Configuration

```ruby
output {
  # Main Elasticsearch output
  elasticsearch {
    hosts => ["${ELASTICSEARCH_HOSTS}"]
    index => "logs-%{[namespace]}-%{+YYYY.MM.dd}"
    user => "${ELASTICSEARCH_USER}"
    password => "${ELASTICSEARCH_PASSWORD}"
    ssl => true
    cacert => "/etc/logstash/certs/ca.crt"
    
    # ILM settings
    ilm_enabled => true
    ilm_rollover_alias => "logs"
    ilm_pattern => "{now/d}-000001"
    ilm_policy => "logs-policy"
  }
  
  # Send alerts to different index
  if "alert" in [tags] {
    elasticsearch {
      hosts => ["${ELASTICSEARCH_HOSTS}"]
      index => "alerts-%{+YYYY.MM.dd}"
      user => "${ELASTICSEARCH_USER}"
      password => "${ELASTICSEARCH_PASSWORD}"
    }
  }
  
  # Forward to Kafka for further processing
  if [type] == "metric" {
    kafka {
      bootstrap_servers => "${KAFKA_BROKERS}"
      topic_id => "processed-metrics"
      codec => json
    }
  }
  
  # Debug output (disable in production)
  if [@metadata][debug] {
    stdout {
      codec => rubydebug
    }
  }
}
```

## Troubleshooting

### Check Logstash Logs

```bash
# View pod logs
oc logs -f deployment/logstash -n <namespace>

# View logs from specific pod
oc logs logstash-pod-xyz -n <namespace>

# View logs with timestamps
oc logs --timestamps deployment/logstash -n <namespace>

# View previous pod logs (after crash)
oc logs --previous logstash-pod-xyz -n <namespace>
```

### Common Issues

#### Pipeline Not Loading
```bash
# Verify ConfigMap is mounted
oc describe pod <logstash-pod> -n <namespace>

# Check ConfigMap content
oc get configmap logstash-pipeline -o yaml -n <namespace>

# Verify syntax
# Exec into pod and test
oc exec -it <logstash-pod> -n <namespace> -- bash
/usr/share/logstash/bin/logstash --config.test_and_exit -f /usr/share/logstash/pipeline/
```

#### Memory/Performance Issues
```bash
# Check resource usage
oc top pod -l app=logstash -n <namespace>

# Adjust JVM heap in deployment
# Edit LS_JAVA_OPTS environment variable
oc set env deployment/logstash LS_JAVA_OPTS="-Xmx2g -Xms2g" -n <namespace>

# Scale replicas for load distribution
oc scale deployment/logstash --replicas=3 -n <namespace>
```

#### Connection Issues
```bash
# Test connectivity from Logstash pod
oc exec -it <logstash-pod> -n <namespace> -- bash
curl -k https://elasticsearch:9200
nc -zv kafka-cluster 9092

# Check secrets are properly mounted
oc exec -it <logstash-pod> -n <namespace> -- env | grep ELASTIC
```

### API Monitoring

```bash
# Check Logstash API (monitoring endpoint)
oc port-forward deployment/logstash 9600:9600 -n <namespace>
curl http://localhost:9600/_node/stats/pipelines?pretty

# Check pipeline status
curl http://localhost:9600/_node/pipelines?pretty
```

### Dead Letter Queue

```bash
# Access DLQ if enabled
oc exec -it <logstash-pod> -n <namespace> -- bash
cd /usr/share/logstash/data/dead_letter_queue
ls -lh

# Replay DLQ events
/usr/share/logstash/bin/logstash -f /path/to/dlq-replay.conf
```

## Testing Pipeline Changes

### Local Testing Pattern

```bash
# 1. Extract current ConfigMap
oc get configmap logstash-pipeline -o yaml > pipeline-backup.yaml

# 2. Create test version locally
cat > test-pipeline.conf <<EOF
input {
  stdin { codec => json }
}
filter {
  # Your filter logic here
}
output {
  stdout { codec => rubydebug }
}
EOF

# 3. Test with Docker locally
docker run --rm -it \
  -v $(pwd)/test-pipeline.conf:/usr/share/logstash/pipeline/test.conf \
  docker.elastic.co/logstash/logstash:8.11.0

# 4. Apply to dev namespace first
oc apply -f updated-pipeline.yaml -n logging-dev

# 5. Monitor for errors
oc logs -f deployment/logstash -n logging-dev

# 6. Promote to production after validation
oc apply -f updated-pipeline.yaml -n logging-prod
```

### Validation Checklist

- [ ] Syntax validation passed
- [ ] Test data processed correctly
- [ ] No performance degradation
- [ ] Error handling works as expected
- [ ] Secrets/credentials properly referenced
- [ ] Index patterns follow naming convention
- [ ] Monitoring shows healthy pipeline
- [ ] Rollback plan prepared

## Security Best Practices

### Secrets Management

```bash
# Create secret for credentials
oc create secret generic logstash-credentials \
  --from-literal=elasticsearch-user=logstash_writer \
  --from-literal=elasticsearch-password='SecurePass123!' \
  -n <namespace>

# Reference in deployment as environment variables
# (See deployment YAML above)

# Never put credentials in ConfigMaps
# Always use Secrets or external secret management (Vault, etc.)
```

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: logstash-netpol
  namespace: logging
spec:
  podSelector:
    matchLabels:
      app: logstash
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: filebeat
    ports:
    - protocol: TCP
      port: 5044
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: elasticsearch
    ports:
    - protocol: TCP
      port: 9200
  - to:
    - podSelector:
        matchLabels:
          app: kafka
    ports:
    - protocol: TCP
      port: 9092
```

## Monitoring and Alerts

### Key Metrics to Monitor

- Pipeline throughput (events/sec)
- Processing latency
- Memory and CPU usage
- Dead letter queue size
- Output connection failures
- Pod restart count

### Prometheus Integration

```yaml
# ServiceMonitor for Prometheus Operator
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: logstash
  namespace: logging
spec:
  selector:
    matchLabels:
      app: logstash
  endpoints:
  - port: http
    interval: 30s
    path: /_node/stats
```

## Common Workflows

### Adding a New Pipeline

1. Create new ConfigMap with pipeline configuration
2. Update Deployment to mount the new ConfigMap
3. Apply changes and monitor rollout
4. Validate data flow to outputs

### Updating Existing Pipeline

1. Backup current ConfigMap
2. Edit ConfigMap with new configuration
3. Test in non-production environment
4. Rollout restart deployment
5. Monitor logs for errors
6. Rollback if issues detected

### Debugging Parse Failures

1. Check logs for grok parse failures
2. Extract sample failed messages
3. Test grok patterns with sample data
4. Update filter configuration
5. Apply and validate

### Scaling Logstash

```bash
# Horizontal scaling
oc scale deployment/logstash --replicas=5 -n <namespace>

# Vertical scaling (resource limits)
oc set resources deployment/logstash \
  --limits=cpu=2000m,memory=4Gi \
  --requests=cpu=1000m,memory=2Gi \
  -n <namespace>
```

## Reference

### Useful Commands

```bash
# Quick reference card
alias ls-config="oc get configmap logstash-pipeline -o yaml"
alias ls-logs="oc logs -f deployment/logstash"
alias ls-restart="oc rollout restart deployment/logstash"
alias ls-status="oc rollout status deployment/logstash"
alias ls-describe="oc describe deployment logstash"
alias ls-exec="oc exec -it deployment/logstash -- bash"
```

### Documentation Links

- Logstash Reference: https://www.elastic.co/guide/en/logstash/current/index.html
- OpenShift ConfigMaps: https://docs.openshift.com/container-platform/latest/nodes/pods/nodes-pods-configmaps.html
- Logstash Performance Tuning: https://www.elastic.co/guide/en/logstash/current/performance-tuning.html
- Plugin Documentation: https://www.elastic.co/guide/en/logstash/current/input-plugins.html

### Tips

- Always test configuration changes in non-production first
- Use config reload feature for minor changes
- Monitor pipeline stats via API before/after changes
- Keep pipelines modular (separate input/filter/output files)
- Document custom grok patterns in separate ConfigMap
- Use environment variables for environment-specific values
- Enable dead letter queue for critical pipelines
- Implement proper error handling and tagging
- Regular review of pipeline performance metrics
- Maintain version control for all ConfigMap configurations
