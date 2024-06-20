#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: acm_phy_layer
# Author: CS6 - 615
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from g4fsk_decoding import g4fsk_decoding  # grc-generated hier_block
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import numpy as np
import physical_layer_transmitter_epy_block_0 as epy_block_0  # embedded python block
import physical_layer_transmitter_epy_block_0_0 as epy_block_0_0  # embedded python block
import physical_layer_transmitter_epy_block_1_0_0 as epy_block_1_0_0  # embedded python block
import physical_layer_transmitter_epy_block_1_0_0_0 as epy_block_1_0_0_0  # embedded python block
import physical_layer_transmitter_epy_block_2_0_0 as epy_block_2_0_0  # embedded python block
import physical_layer_transmitter_taps as taps  # embedded python module
import physical_layer_transmitter_th as th  # embedded python module
import sip



class physical_layer_transmitter(gr.top_block, Qt.QWidget):

    def __init__(self, p_cmd_in=5555, p_cmd_out=5556, p_data_in=5558, p_data_out=5557):
        gr.top_block.__init__(self, "acm_phy_layer", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("acm_phy_layer")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "physical_layer_transmitter")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Parameters
        ##################################################
        self.p_cmd_in = p_cmd_in
        self.p_cmd_out = p_cmd_out
        self.p_data_in = p_data_in
        self.p_data_out = p_data_out

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.samp_rate = samp_rate = 200e3
        self.bandwidth = bandwidth = 25000
        self.repack_size = repack_size = 1
        self.decimation_rx = decimation_rx = samp_rate/(sps*th.modcod(bandwidth, "1"))
        self.decimation = decimation = samp_rate/(sps*th.modcod(bandwidth, "1"))

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source(f"tcp://localhost:{p_cmd_in}", 100, False)
        self.zeromq_req_source_1 = zeromq.req_source(gr.sizeof_gr_complex, 64, 'tcp://localhost:4001', 100, False, (-1), False)
        self.zeromq_req_source_0 = zeromq.req_source(gr.sizeof_char, 1, f"tcp://localhost:{p_data_in}", 100, False, (-1), False)
        self.zeromq_rep_sink_1 = zeromq.rep_sink(gr.sizeof_gr_complex, 64, 'tcp://*:4000', 100, False, (-1), True)
        self.zeromq_rep_sink_0 = zeromq.rep_sink(gr.sizeof_char, 1, f"tcp://*:{p_data_out}", 100, False, (-1), True)
        self.zeromq_pub_msg_sink_0 = zeromq.pub_msg_sink(f"tcp://*:{p_cmd_out}", 100, True)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            (2**12), #size
            window.WIN_RECTANGULAR, #wintype
            0, #fc
            samp_rate, #bw
            "RF_in", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            (2**12), #size
            window.WIN_RECTANGULAR, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.mmse_resampler_xx_1 = filter.mmse_resampler_cc(0, decimation_rx)
        self.mmse_resampler_xx_0 = filter.mmse_resampler_cc(0, (1/decimation))
        self.interp_fir_filter_xxx_0_0 = filter.interp_fir_filter_fff(sps, taps.generate_taps(sps, 0.25))
        self.interp_fir_filter_xxx_0_0.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(sps, taps.generate_taps(sps, 0.5))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.g4fsk_decoding_0 = g4fsk_decoding()
        self.epy_block_2_0_0 = epy_block_2_0_0.blk(fft_size=2**15, bandwidth=25e3, samplerate=samp_rate, addr="snr_meas")
        self.epy_block_1_0_0_0 = epy_block_1_0_0_0.blk(addr='demux_1')
        self.epy_block_1_0_0 = epy_block_1_0_0.blk(addr='mux_1')
        self.epy_block_0_0 = epy_block_0_0.blk(addr='demux', samprate=samp_rate)
        self.epy_block_0 = epy_block_0.blk(addr='mux', samp_rate=samp_rate, bandwidth=bandwidth, sps=4)
        self.digital_symbol_sync_xx_1_0_0_0 = digital.symbol_sync_ff(
            digital.TED_SIGNAL_TIMES_SLOPE_ML,
            sps,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_PFB_NO_MF,
            64,
            [])
        self.digital_symbol_sync_xx_1_0_0 = digital.symbol_sync_ff(
            digital.TED_SIGNAL_TIMES_SLOPE_ML,
            sps,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_PFB_NO_MF,
            64,
            [])
        self.digital_symbol_sync_xx_1_0 = digital.symbol_sync_ff(
            digital.TED_MUELLER_AND_MULLER,
            sps,
            0.1,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_PFB_NO_MF,
            64,
            [])
        self.digital_chunks_to_symbols_xx_1 = digital.chunks_to_symbols_bf([-1.5, -0.5, 0.5, 1.5], 1)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bf([-1, 1], 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bf([-1, 1], 1)
        self.digital_binary_slicer_fb_0_0 = digital.binary_slicer_fb()
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 64)
        self.blocks_vco_c_0 = blocks.vco_c(samp_rate, ((2*np.pi*th.modcod(bandwidth, "9"))/1.5), 0.5)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 64)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, (2**15))
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, sps)
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(8, repack_size, "", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(repack_size, 8, "", False, gr.GR_MSB_FIRST)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_msgpair_to_var_1_0 = blocks.msg_pair_to_var(self.set_decimation_rx)
        self.blocks_msgpair_to_var_1 = blocks.msg_pair_to_var(self.set_decimation)
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_repack_size)
        self.blocks_float_to_uchar_0 = blocks.float_to_uchar(1, 1, 0)
        self.analog_quadrature_demod_cf_2 = analog.quadrature_demod_cf(((samp_rate*2)/(2*np.pi*th.modcod(bandwidth, "9"))))
        self.analog_quadrature_demod_cf_1 = analog.quadrature_demod_cf(1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(((np.pi/2)/sps))
        self.analog_frequency_modulator_fc_0_0 = analog.frequency_modulator_fc(((np.pi / 2) / sps))
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(((np.pi / 2) / sps))


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'repack_out'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.msg_connect((self.epy_block_0, 'decim_out'), (self.blocks_msgpair_to_var_1, 'inpair'))
        self.msg_connect((self.epy_block_0, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.epy_block_0_0, 'decim_out'), (self.blocks_msgpair_to_var_1_0, 'inpair'))
        self.msg_connect((self.epy_block_0_0, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.epy_block_1_0_0, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.epy_block_1_0_0_0, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.epy_block_2_0_0, 'msg_out'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_0, 'msg_in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_0_0, 'msg_in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_1_0_0, 'msg_in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_1_0_0_0, 'msg_in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_2_0_0, 'msg_in'))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.epy_block_1_0_0, 2))
        self.connect((self.analog_frequency_modulator_fc_0_0, 0), (self.epy_block_1_0_0, 1))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.digital_symbol_sync_xx_1_0, 0))
        self.connect((self.analog_quadrature_demod_cf_1, 0), (self.digital_symbol_sync_xx_1_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_2, 0), (self.digital_symbol_sync_xx_1_0_0_0, 0))
        self.connect((self.blocks_float_to_uchar_0, 0), (self.epy_block_1_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.zeromq_rep_sink_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.analog_frequency_modulator_fc_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.epy_block_2_0_0, 0))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.zeromq_rep_sink_1, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_vco_c_0, 0), (self.epy_block_1_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.mmse_resampler_xx_1, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.epy_block_1_0_0_0, 2))
        self.connect((self.digital_binary_slicer_fb_0_0, 0), (self.epy_block_1_0_0_0, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1, 0), (self.interp_fir_filter_xxx_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_1_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.digital_symbol_sync_xx_1_0_0, 0), (self.digital_binary_slicer_fb_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_1_0_0_0, 0), (self.g4fsk_decoding_0, 0))
        self.connect((self.epy_block_0, 2), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.epy_block_0, 1), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.epy_block_0, 0), (self.digital_chunks_to_symbols_xx_1, 0))
        self.connect((self.epy_block_0_0, 2), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.epy_block_0_0, 1), (self.analog_quadrature_demod_cf_1, 0))
        self.connect((self.epy_block_0_0, 0), (self.analog_quadrature_demod_cf_2, 0))
        self.connect((self.epy_block_1_0_0, 0), (self.mmse_resampler_xx_0, 0))
        self.connect((self.epy_block_1_0_0_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.g4fsk_decoding_0, 0), (self.blocks_float_to_uchar_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.interp_fir_filter_xxx_0_0, 0), (self.blocks_vco_c_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.blocks_stream_to_vector_1, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.mmse_resampler_xx_1, 0), (self.epy_block_0_0, 0))
        self.connect((self.zeromq_req_source_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.zeromq_req_source_1, 0), (self.blocks_vector_to_stream_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "physical_layer_transmitter")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_p_cmd_in(self):
        return self.p_cmd_in

    def set_p_cmd_in(self, p_cmd_in):
        self.p_cmd_in = p_cmd_in

    def get_p_cmd_out(self):
        return self.p_cmd_out

    def set_p_cmd_out(self, p_cmd_out):
        self.p_cmd_out = p_cmd_out

    def get_p_data_in(self):
        return self.p_data_in

    def set_p_data_in(self, p_data_in):
        self.p_data_in = p_data_in

    def get_p_data_out(self):
        return self.p_data_out

    def set_p_data_out(self, p_data_out):
        self.p_data_out = p_data_out

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_decimation(self.samp_rate/(self.sps*th.modcod(self.bandwidth, "1")))
        self.set_decimation_rx(self.samp_rate/(self.sps*th.modcod(self.bandwidth, "1")))
        self.analog_frequency_modulator_fc_0.set_sensitivity(((np.pi / 2) / self.sps))
        self.analog_frequency_modulator_fc_0_0.set_sensitivity(((np.pi / 2) / self.sps))
        self.analog_quadrature_demod_cf_0.set_gain(((np.pi/2)/self.sps))
        self.blocks_repeat_0.set_interpolation(self.sps)
        self.digital_symbol_sync_xx_1_0.set_sps(self.sps)
        self.digital_symbol_sync_xx_1_0_0.set_sps(self.sps)
        self.digital_symbol_sync_xx_1_0_0_0.set_sps(self.sps)
        self.interp_fir_filter_xxx_0.set_taps(taps.generate_taps(self.sps, 0.5))
        self.interp_fir_filter_xxx_0_0.set_taps(taps.generate_taps(self.sps, 0.25))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_decimation(self.samp_rate/(self.sps*th.modcod(self.bandwidth, "1")))
        self.set_decimation_rx(self.samp_rate/(self.sps*th.modcod(self.bandwidth, "1")))
        self.analog_quadrature_demod_cf_2.set_gain(((self.samp_rate*2)/(2*np.pi*th.modcod(self.bandwidth, "9"))))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.epy_block_0.samp_rate = self.samp_rate
        self.epy_block_2_0_0.samplerate = self.samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.set_decimation(self.samp_rate/(self.sps*th.modcod(self.bandwidth, "1")))
        self.set_decimation_rx(self.samp_rate/(self.sps*th.modcod(self.bandwidth, "1")))
        self.analog_quadrature_demod_cf_2.set_gain(((self.samp_rate*2)/(2*np.pi*th.modcod(self.bandwidth, "9"))))
        self.epy_block_0.bandwidth = self.bandwidth

    def get_repack_size(self):
        return self.repack_size

    def set_repack_size(self, repack_size):
        self.repack_size = repack_size
        self.blocks_repack_bits_bb_0.set_k_and_l(self.repack_size,8)
        self.blocks_repack_bits_bb_0_0.set_k_and_l(8,self.repack_size)

    def get_decimation_rx(self):
        return self.decimation_rx

    def set_decimation_rx(self, decimation_rx):
        self.decimation_rx = decimation_rx
        self.mmse_resampler_xx_1.set_resamp_ratio(self.decimation_rx)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.mmse_resampler_xx_0.set_resamp_ratio((1/self.decimation))



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--p-cmd-in", dest="p_cmd_in", type=intx, default=5000,
        help="Set cmd_port_in [default=%(default)r]")
    parser.add_argument(
        "--p-cmd-out", dest="p_cmd_out", type=intx, default=5001,
        help="Set cmd_port_out [default=%(default)r]")
    parser.add_argument(
        "-i", "--p-data-in", dest="p_data_in", type=intx, default=5002,
        help="Set data_port_in [default=%(default)r]")
    parser.add_argument(
        "-o", "--p-data-out", dest="p_data_out", type=intx, default=5003,
        help="Set data_port_out [default=%(default)r]")
    return parser



def main(top_block_cls=physical_layer_transmitter, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(p_cmd_in=options.p_cmd_in, p_cmd_out=options.p_cmd_out, p_data_in=options.p_data_in, p_data_out=options.p_data_out)

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
