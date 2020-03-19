/*
 * Copyright (C) 2019 National Institute of Informatics
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

package jp.ad.sinet.stream.spi;

import jp.ad.sinet.stream.api.Consistency;
import jp.ad.sinet.stream.api.ValueType;
import jp.ad.sinet.stream.utils.MessageReaderFactory;
import lombok.Data;
import lombok.RequiredArgsConstructor;

import java.time.Duration;
import java.util.List;
import java.util.Map;

@Data
@RequiredArgsConstructor
public class ReaderParameters implements SinetStreamParameters {
    private final String service;
    private final Consistency consistency;
    private final ValueType valueType;
    private final Map<String, Object> config;
    private final boolean dataEncryption;

    private final List<String> topics;
    private final Duration receiveTimeout;

    private String clientId;

    public ReaderParameters(MessageReaderFactory<?> builder) {
        this.service = builder.getService();
        this.topics = builder.getTopics();
        this.consistency = builder.getConsistency();
        this.config = builder.getParameters();
        this.valueType = builder.getValueType();
        this.receiveTimeout = builder.getReceiveTimeout();
        this.clientId = builder.getClientId();
        this.dataEncryption = builder.getDataEncryption();
    }
}
