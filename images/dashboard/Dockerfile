FROM python:3.5.1-onbuild

EXPOSE 9181
CMD ["rq-dashboard", "--port", "9181", \
                     "--redis-host", "redis-master", \
	"--redis-port", "6379"]
