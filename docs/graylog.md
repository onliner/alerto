## 🧭 Alerto Integration Setup Guide

### Step 1: Create the Alerto Stream

1. Navigate to **Streams → Create Stream** in Graylog.
2. **Stream name:** `Alerto`
3. **Description:** `Stream for Telegram alerts — collects important messages from multiple streams.`  
4. Enable the option **"Remove matches from 'Default Stream'."**
   - Ensures that messages routed to Alerto are excluded from the Default Stream, keeping it clean and preventing duplication.  
5. Click **Save** to create the stream.
6. Once created, start the stream if it’s shown as *Paused*:  
   - **More actions → Start stream**.
   - The status should change to *Running*.  

**Result:**  
You now have a dedicated stream named **Alerto**, which will receive only filtered, important log messages intended for Telegram notifications.

### Step 2: Create and connect a Pipeline

1. Go to **System → Pipelines → Manage pipelines → Create pipeline.**  
   - **Name:** `Route logs to Alerto`
   - **Description:** `Routes important application logs to the Alerto stream based on severity and tags.`  
2. Open the pipeline and click **Edit connections.**
3. In the list of streams, select **Application**.
4. Click **Update connections.**

### Step 3: Use Stage 0 for routing rules

When a new pipeline is created, **Stage 0** is added automatically.  
There’s no need to create it manually — this stage will hold the routing rules.  
Your first rule will execute here as soon as messages from the *Application* stream enter the pipeline.

### Step 4: Create a Pipeline Rule

1. Go to **System → Pipelines → Rules → Create Rule → Use Source Code Editor.**
   - **Rule name:** `alerto_route_backend_errors`  
   - **Description:** `Routes relevant application logs to the Alerto stream based on severity and tag filters.`
2. Create rule with code:

```groovy
rule "alerto_route_backend_errors"
when
  // Level must be <= 4 (error, warning, etc.)
  to_long(get_field("level")) <= 4 &&

  // Tag must be in the allowed list
  array_contains(["application_log", "php_error"], get_field("tag"))
then
  let hash = murmur3_128(to_string($message.message));

  // Add a field for easier filtering and tracking
  set_field("hash", hash);
  set_field("type", "backend");
  set_field("title", "❗️ Application Error");

  // Route the message to the Alerto stream
  route_to_stream("Alerto");
end
```

#### Additional examples:

#### Route by message text (case-insensitive match)

```groovy
rule "alerto_route_contains_errors"
when
  // Message contains WARN or ERROR (case-insensitive)
  (
    contains(to_string($message.message), "warn", true) ||
    contains(to_string($message.message), "error", true)
  )
then
  let hash = murmur3_128(to_string($message.message));

  set_field("hash", hash);
  set_field("type", "backend");
  set_field("title", "❗️ Application Error");

  route_to_stream("Alerto");
end
```

#### Same logic using a regex (optional)

```groovy
rule "alerto_route_text_regex"
when
  // Case-insensitive match for 'warn' or 'error' anywhere in the message
  to_bool(regex("(?i)(warn|error)", to_string($message.message)).matches)
then
  let hash = murmur3_128(to_string($message.message));

  set_field("hash", hash);
  set_field("type", "backend");
  set_field("title", "❗️ Application Error");

  route_to_stream("Alerto");
end
```

> [!NOTE]  
> For more details on the Pipeline Rule language (functions, regex, routing, etc.), see the official docs:  
> [**Pipeline Rule Logic →**](https://go2docs.graylog.org/current/making_sense_of_your_log_data/rules.html)

### Step 5: Attach the Rule to Stage 0

1. Open your pipeline **Route logs to Alerto.**
2. Under **Stage 0**, click **Edit.**
3. In **Stage rules**, select **alerto_route_backend_errors.**  
4. Set **Continue processing on next stage when:** *At least one of the rules on this stage matches the message.*  
5. Click **Update** to save the stage.

**Result:**  
Stage 0 now evaluates the rule `alerto_route_backend_errors`.  
If a message from the *Application* stream meets the defined conditions, it will be routed automatically to the **Alerto** stream.

> [!TIP]  
> In the future, you can add additional rules to the same pipeline to filter and route messages from other streams into **Alerto**.  
> For example, rules handling network, kubernetes, or frontend errors can reuse this pipeline to send all critical logs to one unified alert stream.

### Step 6: Create a Notification

Before creating the Event Definition, you need a reusable notification.

1. Go to **Alerts → Notifications → Create.**
2. **Title:** `Alerto`
3. **Description:** `HTTP notification to alerto.onliner.by that sends backend alerts to the Telegram chat.`  
4. **Notification Type:** `HTTP Notification`
5. **URL:** `https://alerto.test.com`

#### 🔐 Optional: Add Authentication Headers

If your endpoint is protected by an access token (see `.env` → `AUTH_TOKEN`),  
you can configure Graylog to include authorization headers automatically.

Fill in the fields as follows:

- **API Key:** `Authorization`
- **API Secret:** `Bearer <auth token>`
- **Send API Key/Secret as Header:** Yes

> Replace `<auth token>` with your secret value from the `.env` file —  
> the same value defined as the `AUTH_TOKEN` environment variable when running Alerto.

> [!CAUTION]  
> **Keep your token secret — anyone with this key can send alerts directly to your webhook.**

**Result:**  
You now have a reusable HTTP notification named Alerto, which delivers alert payloads to your webhook.  
If authentication was configured, Graylog adds this header to each request:

```http
Authorization: Bearer <auth token>
```

### Step 7: Create an Event Definition

1. Go to **Alerts → Event Definitions → Create.**
2. **Title:** `Alerto`
   **Description:** `Triggers notifications for messages routed to the Alerto stream.`  
3. **Condition Type:** *Filter & Aggregation*
4. **Filter configuration:**
   - **Search Query:** `*`
   - **Streams:** `Alerto`
   - **Search within the last:** `1 minute`  
   - **Execute search every:** `1 minute`
   - **Create events for definition if filter has results:** Yes  
   - **Event limit:** `100`
5. **Add custom fields:**

> [!IMPORTANT]  
> Add the following custom fields to enrich event data.  
> These fields are used in notifications and make it easier to identify the affected project, message, and severity level.

| Field Name | Use Field as Event Key | Set Value From | Template            |
|------------|------------------------|----------------|---------------------|
| `hash`     | ✅ Yes                 | Template       | `${source.hash}`    |
| `title`    | ❌ No                  | Template       | `${source.title}`   |
| `project`  | ❌ No                  | Template       | `${source.project}` |
| `message`  | ❌ No                  | Template       | `${source.message}` |

6. **Notifications:** Add → Select **Alerto**.
7. **Configure notification:**
   - **Grace Period:** `10 seconds`
   - **Backlog:** `1`
8. Click **Create event definition.**

**Result:**  
Graylog now generates events and triggers the **Alerto** HTTP notification for any messages arriving in the Alerto stream.
