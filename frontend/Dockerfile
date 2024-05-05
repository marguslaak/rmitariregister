FROM node:21-alpine as build
ARG VITE_API_URL
WORKDIR /app
COPY package*.json ./
RUN npm ci
RUN if [ -n "$VITE_API_URL"] ; then echo -n 'VITE_API_URL="'"$VITE_API_URL"'"' > ./.env ; fi
COPY . ./
RUN npm run build

FROM nginx:stable
COPY nginx/default.conf /etc/nginx/conf.d/
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
