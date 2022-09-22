#!/usr/bin/env python3
# pylint: disable=I0011
# pylint: disable=C0103
# pylint: disable=C0325
# pylint: disable=C0413
"""Encapsulated logging"""

import logging
import sys
from logging.handlers import RotatingFileHandler


class Logger:
	"""Plain logging - encapsulated on the basis that future implementations will adjust logging requirements"""
	c_loggingConfFile = "logging.conf"
	c_loggingOutput = "arp"
	# change the logging format here, using this for the elements:
	# https://docs.python.org/3/library/logging.html#logrecord-attributes
	c_loggingFormat = "%(asctime)s: [%(levelname)s] %(name)s [%(lineno)s] %(funcName)s) %(message)s"

	def __init__(self, logLevel = logging.debug, enableStdOut = False):
		"""Ctor"""
		logging.root.handlers = []

		# NOTE: simple version for reference
		# logging.basicConfig(
		# 	filename=self.c_loggingOutput, 
		# 	format=self.c_loggingFormat, 
		# 	encoding="utf-8", level=logLevel
		# )

		self.pipe = logging.getLogger("ARP-V %s" % self.__class__.__name__)

		# Python doesn't really do threading, so just make sure handlers are not always used across instances
		if len(self.pipe.handlers) == 0:
			if enableStdOut:
				direct = logging.StreamHandler(sys.stdout)
				direct.setFormatter(logging.Formatter(self.c_loggingFormat))
				self.pipe.addHandler(direct)

			rotated = logging.handlers.RotatingFileHandler(
				"{!s}/{!s}.log".format(".", self.c_loggingOutput or self.__class__.__name__),
				maxBytes=1024<<8,
				backupCount=4
			)
			rotated.setFormatter(logging.Formatter(self.c_loggingFormat))
			self.pipe.setLevel(logLevel)
			self.pipe.addHandler(rotated)

	def __del__(self):
		"""Dtor to counter GC issues in specific circumstances"""
		# NOTE: not implemented in this version

	def log(self, message: str, logLevel = logging.debug()):
		"""Logs a plain message with default log level DEBUG"""
		
		## NOTE: match keyword requires python 3.10
		# match logLevel:
		# 	case logging.INFO:
		# 		self.pipe.info(message)
		# 	case logging.WARN:
		# 		self.pipe.warn(message)
		# 	case logging.ERROR:
		# 		self.pipe.error(message)
		# 	case _:
		# 		self.pipe.debug(message)

		if logLevel == logging.ERROR:
			self.pipe.error(message)
		elif logLevel == logging.INFO:
			self.pipe.info(message)
		else:
			self.pipe.debug(message)
			
