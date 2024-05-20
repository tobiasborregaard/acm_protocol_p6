#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: jonasj2001
# GNU Radio version: 3.10.5.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import test_epy_block_0 as epy_block_0  # embedded python block
import test_epy_block_0_0 as epy_block_0_0  # embedded python block
import test_epy_block_0_1 as epy_block_0_1  # embedded python block
import test_epy_block_0_1_0 as epy_block_0_1_0  # embedded python block
import test_epy_block_0_2 as epy_block_0_2  # embedded python block



from gnuradio import qtgui

class test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "test")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source('tcp://localhost:5555', 100, False)
        self.zeromq_req_source_0 = zeromq.req_source(gr.sizeof_char, 1, 'tcp://localhost:5558', 100, False, (-1))
        self.zeromq_rep_sink_0 = zeromq.rep_sink(gr.sizeof_char, 1, 'tcp://*:5557', 100, False, (-1))
        self.zeromq_pub_msg_sink_0 = zeromq.pub_msg_sink('tcp://*:5556', 100, True)
        self.epy_block_0_2 = epy_block_0_2.blk(addr="mux")
        self.epy_block_0_1_0 = epy_block_0_1_0.blk(addr="mux_1")
        self.epy_block_0_1 = epy_block_0_1.blk(addr="demux_1")
        self.epy_block_0_0 = epy_block_0_0.blk(addr='snr_meas')
        self.epy_block_0 = epy_block_0.blk(addr="demux")
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, 50000,True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.epy_block_0_0, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.epy_block_0_1, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.epy_block_0_1_0, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.epy_block_0_2, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_0, 'msg_in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_0_0, 'msg_in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_0_1, 'msg_in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_0_1_0, 'msg_in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_0_2, 'msg_in'))
        self.connect((self.blocks_throttle_0, 0), (self.zeromq_rep_sink_0, 0))
        self.connect((self.zeromq_req_source_0, 0), (self.blocks_throttle_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate




def main(top_block_cls=test, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
