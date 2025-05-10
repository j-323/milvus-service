{{- define "service3-embed.name" -}}
{{ .Chart.Name }}
{{- end -}}

{{- define "service3-embed.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end -}}