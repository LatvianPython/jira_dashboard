FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY --from=jira_dashboard_client:latest /app/dist /app
