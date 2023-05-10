---
description: Use managed Grafana, or build custom dashboards with a self-hosted instance
---

# Grafana

## Managed Grafana <a href="#grafana" id="grafana"></a>

CoreWeave provides a managed Grafana instance where you can view predefined dashboards with compute and storage summaries, and detailed reports of the GPUs, CPUs, memory, and network activity for each Pod.&#x20;

To access the managed Grafana instance, use the menu in the Account Details section of [CoreWeave Cloud](https://cloud.coreweave.com) or navigate directly to [https://grafana.coreweave.com](https://grafana.coreweave.com).

<figure><img src="../.gitbook/assets/image (24) (4).png" alt="Screenshot of Grafana menu in CoreWeave Cloud"><figcaption><p>Grafana menu</p></figcaption></figure>

You cannot modify these dashboards or create new ones in this Grafana instance. However, if you'd like complete control, deploy your own self-hosted Grafana instance on CoreWeave Cloud.

## Self-hosted Grafana

To build custom dashboards from CoreWeave's [Prometheus metrics](../../coreweave-kubernetes/prometheus/), you can deploy your own Grafana instance with [CoreWeave Apps](https://apps.coreweave.com).

<figure><img src="../.gitbook/assets/image (21) (3).png" alt="Grafana in the application catalog"><figcaption><p>Grafana</p></figcaption></figure>

### How to deploy Grafana

1. Navigate to [CoreWeave Applications](https://apps.coreweave.com), then click **Catalog**.
2. Search for Grafana, then click it to access the deployment screen.
3. Click **Deploy** in the upper-right corner.
4. Give it a meaningful name.
5. In most cases, you'll want to leave **Expose to the Public via Ingress** selected.
6. Click **Deploy**.

Wait for the Pods to deploy, then click the Ingress URL to log in with the username and password in the upper-right corner.

<figure><img src="../.gitbook/assets/image (13) (5).png" alt="Screenshot of deployment screen"><figcaption><p>Deployment screen</p></figcaption></figure>

### Connect to Prometheus

Our Prometheus scraping service offers many useful [billing metrics](../../coreweave-kubernetes/prometheus/useful-metrics.md) you can use in your self-hosted Grafana instance. If you have an on-premise Grafana instance, you can follow these same steps to connect to CoreWeave's Prometheus service.&#x20;

1.  In your Grafana instance, go to **Configuration -> Data Sources** in the lower left menu.\


    <figure><img src="../.gitbook/assets/image (9).png" alt="Data sources menu"><figcaption><p>Data sources menu</p></figcaption></figure>


2. Click **Add New Datasource** and select **Prometheus**.
3. Set the **Name** to **CoreWeave**.
4. Set the **URL** to `https://prometheus.ord1.coreweave.com`.
5. Click **Add Header** in the **Custom HTTP Headers** section.
6.  Set the following values for **Custom HTTP Header.** \
    \
    **Header**: `Authorization` \
    **Value**: `Bearer [my-token]`\
    \
    Replace `[my-token]` with your API Access token.\


    <figure><img src="../.gitbook/assets/image (11).png" alt="Connection settings"><figcaption><p>Connection settings</p></figcaption></figure>
7.  Click **Save & Test** at the bottom of the page to verify and save the new datasource.\
    \


    <figure><img src="../.gitbook/assets/image (8).png" alt="Successful connection"><figcaption><p>Successful connection</p></figcaption></figure>

### How to find your API Access Token

If you don't have a token, you can generate a new one on the [API Access](https://cloud.coreweave.com/api-access) page. If you've already configured Kubernetes, your token is in the `users` section of `kubeconfig`. &#x20;

You can view your unredacted `kubeconfig` using `kubectl`.

```
kubectl config view --raw
```

Here's a redacted example:

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://k8s.ord1.coreweave.com
  name: coreweave
contexts:
- context:
    cluster: coreweave
    namespace: tenant-EXAMPLE
    user: token-EXAMPLE-USER
  name: coreweave
current-context: coreweave
kind: Config
preferences: {}
users:
- name: token-EXAMPLE-USER
  user:
    token: REDACTED
```

The API Access token, which is `REDACTED` in this example, is located in the `users` section at the bottom.

If you have more than one context in your kubeconfig, make sure to choose the token for your desired namespace.

## Billing metrics

If you are building a Grafana dashboard for the first time, we suggest reading [Build your first dashboard](https://grafana.com/docs/grafana/latest/getting-started/build-first-dashboard/) at Grafana Labs.

If you have some experience with Grafana and need to know where to find the metrics, look for the  `billing` metrics in the CoreWeave datasource. You do not need to filter the namespace when adding these metrics to a dashboard.

<figure><img src="../.gitbook/assets/image (4).png" alt="Billing metrics"><figcaption><p>Billing metrics</p></figcaption></figure>

{% hint style="success" %}
There's no need to filter the `namespace` label to your namespace for any metric. It will be automatically inserted on all queries received.
{% endhint %}

For more information about our Prometheus scraping service, refer to our [Metrics](../../coreweave-kubernetes/prometheus/) article.