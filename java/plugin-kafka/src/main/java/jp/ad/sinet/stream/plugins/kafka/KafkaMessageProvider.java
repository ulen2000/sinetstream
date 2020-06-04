/*
 * Copyright (C) 2020 National Institute of Informatics
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

package jp.ad.sinet.stream.plugins.kafka;

import jp.ad.sinet.stream.spi.*;
import lombok.extern.java.Log;

@Log
public class KafkaMessageProvider implements MessageWriterProvider, MessageReaderProvider, AsyncMessageWriterProvider, AsyncMessageReaderProvider {

    @Override
    public PluginMessageWriter getWriter(WriterParameters params) {
        log.fine(() -> "KAFKA getWriter: " + params.toString());
        return new KafkaMessageWriter(params);
    }

    @Override
    public PluginMessageReader getReader(ReaderParameters params) {
        log.fine(() -> "KAFKA getReader: " + params.toString());
        return new KafkaMessageReader(params);
    }

    @Override
    public PluginAsyncMessageWriter getAsyncWriter(WriterParameters params) {
        log.fine(() -> "KAFKA getAsyncWriter: " + params.toString());
        return new KafkaAsyncMessageWriter(params);
    }

    @Override
    public PluginAsyncMessageReader getAsyncReader(ReaderParameters params) {
        log.fine(() -> "KAFKA getAsyncReader: " + params.toString());
        return new KafkaAsyncMessageReader(params);
    }

    @Override
    public String getType() {
        return "kafka";
    }
}
